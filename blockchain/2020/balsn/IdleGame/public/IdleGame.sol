pragma solidity =0.5.17;

import "./Tokens.sol";

contract BalsnToken is ERC20 {
    uint randomNumber = RN;
    address public owner;
    
    constructor(uint initialValue) public ERC20("BalsnToken", "BSN") {
        owner = msg.sender;
        _mint(msg.sender, initialValue);
    }
    
    function giveMeMoney() public {
        require(balanceOf(msg.sender) == 0, "BalsnToken: you're too greedy");
        _mint(msg.sender, 1);
    }
}

contract IdleGame is FlashERC20, ContinuousToken {
    uint randomNumber = RN;
    address public owner;
    BalsnToken public BSN;
    mapping(address => uint) public startTime;
    mapping(address => uint) public level;
    
    event GetReward(address, uint);
    event LevelUp(address);
    event BuyGamePoints(address, uint, uint);
    event SellGamePoints(address, uint, uint);
    event SendFlag(address);
    
    constructor (address BSNAddr, uint32 reserveRatio) public ContinuousToken(reserveRatio) ERC20("IdleGame", "IDL") {
        owner = msg.sender;
        BSN = BalsnToken(BSNAddr);
        _mint(msg.sender, 0x9453 * scale);
    }
    
    function getReward() public returns (uint) {
        uint points = block.timestamp.sub(startTime[msg.sender]);
        points = points.add(level[msg.sender]).mul(points);
        _mint(msg.sender, points);
        startTime[msg.sender] = block.timestamp;
        emit GetReward(msg.sender, points);
        return points;
    }
    
    function levelUp() public {
        _burn(msg.sender, level[msg.sender]);
        level[msg.sender] = level[msg.sender].add(1);
        emit LevelUp(msg.sender);
    }
    
    function buyGamePoints(uint amount) public returns (uint) {
        uint bought = _continuousMint(amount);
        BSN.transferFrom(msg.sender, address(this), amount);
        _mint(msg.sender, bought);
        emit BuyGamePoints(msg.sender, amount, bought);
        return bought;
    }
    
    function sellGamePoints(uint amount) public returns (uint) {
        uint bought = _continuousBurn(amount);
        _burn(msg.sender, amount);
        BSN.transfer(msg.sender, bought);
        emit SellGamePoints(msg.sender, bought, amount);
        return bought;
    }
    
    function giveMeFlag() public {
        _burn(msg.sender, (10 ** 8) * scale);
        Setup(owner).giveMeFlag();
        emit SendFlag(msg.sender);
    }
}

contract Setup {
    uint randomNumber = RN;
    bool public sendFlag = false;
    BalsnToken public BSN;
    IdleGame public IDL;
    
    constructor() public {
        uint initialValue = 15000000 * (10 ** 18);
        BSN = new BalsnToken(initialValue);
        IDL = new IdleGame(address(BSN), 999000);
        BSN.approve(address(IDL), uint(-1));
        IDL.buyGamePoints(initialValue);
    }
    
    function giveMeFlag() public {
        require(msg.sender == address(IDL), "Setup: sender incorrect");
        sendFlag = true;
    }
}
