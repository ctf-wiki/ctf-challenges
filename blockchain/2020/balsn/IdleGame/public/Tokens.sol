pragma solidity =0.5.17;

/**
 * @dev Wrappers over Solidity's arithmetic operations with added overflow checks.
 * Modified from the original
 * https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/math/SafeMath.sol
 */
library SafeMath {
    function add(uint a, uint b) internal pure returns (uint) {
        uint c = a + b;
        require(c >= a, "SafeMath: addition overflow");
        return c;
    }

    function sub(uint a, uint b) internal pure returns (uint) {
        return sub(a, b, "SafeMath: subtraction overflow");
    }

    function sub(uint a, uint b, string memory errorMessage) internal pure returns (uint) {
        require(b <= a, errorMessage);
        uint c = a - b;
        return c;
    }

    function mul(uint a, uint b) internal pure returns (uint) {
        if (a == 0) {
            return 0;
        }
        uint c = a * b;
        require(c / a == b, "SafeMath: multiplication overflow");
        return c;
    }

    function div(uint a, uint b) internal pure returns (uint) {
        return div(a, b, "SafeMath: division by zero");
    }

    function div(uint a, uint b, string memory errorMessage) internal pure returns (uint) {
        require(b > 0, errorMessage);
        uint c = a / b;
        return c;
    }
}

/**
 * @dev Interface of the ERC20 standard as defined in the EIP.
 * Modified from the original
 * https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol
 */
interface IERC20 {
    function totalSupply() external view returns (uint);
    function balanceOf(address account) external view returns (uint);
    function transfer(address recipient, uint amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint);
    function approve(address spender, uint amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint amount) external returns (bool);
    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed spender, uint value);
}

/**
 * @dev Implementation of the IERC20 interface.
 * Modified from the original
 * https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol
 */
contract ERC20 is IERC20 {
    using SafeMath for uint;

    string private _name;
    string private _symbol;
    uint8 private _decimals;
    uint private _totalSupply;
    mapping (address => uint) private _balances;
    mapping (address => mapping (address => uint)) private _allowances;

    constructor (string memory name, string memory symbol) public {
        _name = name;
        _symbol = symbol;
        _decimals = 18;
    }

    function name() public view returns (string memory) {
        return _name;
    }

    function symbol() public view returns (string memory) {
        return _symbol;
    }

    function decimals() public view returns (uint8) {
        return _decimals;
    }

    function totalSupply() public view returns (uint) {
        return _totalSupply;
    }

    function balanceOf(address account) public view returns (uint) {
        return _balances[account];
    }

    function transfer(address recipient, uint amount) public returns (bool) {
        _transfer(msg.sender, recipient, amount);
        return true;
    }

    function allowance(address owner, address spender) public view returns (uint) {
        return _allowances[owner][spender];
    }

    function approve(address spender, uint amount) public returns (bool) {
        _approve(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address sender, address recipient, uint amount) public returns (bool) {
        _transfer(sender, recipient, amount);
        _approve(sender, msg.sender, _allowances[sender][msg.sender].sub(amount, "ERC20: transfer amount exceeds allowance"));
        return true;
    }

    function increaseAllowance(address spender, uint addedValue) public returns (bool) {
        _approve(msg.sender, spender, _allowances[msg.sender][spender].add(addedValue));
        return true;
    }

    function decreaseAllowance(address spender, uint subtractedValue) public returns (bool) {
        _approve(msg.sender, spender, _allowances[msg.sender][spender].sub(subtractedValue, "ERC20: decreased allowance below zero"));
        return true;
    }

    function _transfer(address sender, address recipient, uint amount) internal {
        require(sender != address(0), "ERC20: transfer from the zero address");
        require(recipient != address(0), "ERC20: transfer to the zero address");

        _balances[sender] = _balances[sender].sub(amount, "ERC20: transfer amount exceeds balance");
        _balances[recipient] = _balances[recipient].add(amount);
        emit Transfer(sender, recipient, amount);
    }

    function _mint(address account, uint amount) internal {
        require(account != address(0), "ERC20: mint to the zero address");

        _totalSupply = _totalSupply.add(amount);
        _balances[account] = _balances[account].add(amount);
        emit Transfer(address(0), account, amount);
    }

    function _burn(address account, uint amount) internal {
        require(account != address(0), "ERC20: burn from the zero address");

        _balances[account] = _balances[account].sub(amount, "ERC20: burn amount exceeds balance");
        _totalSupply = _totalSupply.sub(amount);
        emit Transfer(account, address(0), amount);
    }

    function _approve(address owner, address spender, uint amount) internal {
        require(owner != address(0), "ERC20: approve from the zero address");
        require(spender != address(0), "ERC20: approve to the zero address");

        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }
}

/**
 * @dev Modified from the original
 * https://github.com/Austin-Williams/flash-mintable-tokens/blob/master/FlashERC20/FlashERC20.sol
 */
interface IBorrower {
    function executeOnFlashMint(uint amount) external;
}

contract FlashERC20 is ERC20 {
    event FlashMint(address to, uint amount);

    function flashMint(uint amount) external {
        _mint(msg.sender, amount);
        IBorrower(msg.sender).executeOnFlashMint(amount);
        _burn(msg.sender, amount);
        emit FlashMint(msg.sender, amount);
    }
}

/**
 * @dev Modified from the original
 * https://github.com/yosriady/continuous-token/blob/master/contracts/token/ContinuousToken.sol
 */
interface BancorBondingCurve {
    function calculatePurchaseReturn(uint _supply,  uint _reserveBalance, uint32 _reserveRatio, uint _depositAmount) external view returns (uint);
    function calculateSaleReturn(uint _supply, uint _reserveBalance, uint32 _reserveRatio, uint _sellAmount) external view returns (uint);
}

contract ContinuousToken is ERC20 {
    using SafeMath for uint;

    BancorBondingCurve public constant BBC = BancorBondingCurve(0xF88212805fE6e37181DE56440CF350817FF87130);
    uint public scale = 10 ** 18;
    uint public reserveBalance = 10 ** 15;
    uint32 public reserveRatio;

    event ContinuousMint(address sender, uint amount, uint deposit);
    event ContinuousBurn(address sender, uint amount, uint reimbursement);

    constructor(uint32 _reserveRatio) public {
        reserveRatio = _reserveRatio;
    }

    function calculateContinuousMintReturn(uint _amount) public view returns (uint mintAmount) {
        return BBC.calculatePurchaseReturn(totalSupply(), reserveBalance, reserveRatio, _amount);
    }

    function calculateContinuousBurnReturn(uint _amount) public view returns (uint burnAmount) {
        return BBC.calculateSaleReturn(totalSupply(), reserveBalance, reserveRatio, _amount);
    }

    function _continuousMint(uint _deposit) internal returns (uint) {
        require(_deposit > 0, "ContinuousToken: Deposit must be non-zero.");
        uint amount = calculateContinuousMintReturn(_deposit);
        reserveBalance = reserveBalance.add(_deposit);
        emit ContinuousMint(msg.sender, amount, _deposit);
        return amount;
    }

    function _continuousBurn(uint _amount) internal returns (uint) {
        require(_amount > 0, "ContinuousToken: Amount must be non-zero.");
        uint reimburseAmount = calculateContinuousBurnReturn(_amount);
        reserveBalance = reserveBalance.sub(reimburseAmount);
        emit ContinuousBurn(msg.sender, _amount, reimburseAmount);
        return reimburseAmount;
    }
}
