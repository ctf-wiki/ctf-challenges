/**
 *Submitted for verification at Etherscan.io on 2019-11-18
*/

pragma solidity ^0.4.24;
// Wow. Welcome to D^3CTF2019

library SafeMath {

    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }

        uint256 c = a * b;
        require(c / a == b);

        return c;
    }

    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b > 0); 
        uint256 c = a / b;

        return c;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a);
        uint256 c = a - b;

        return c;
    }

    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a);

        return c;
    }
}

contract ERC20{
    using SafeMath for uint256;

    mapping (address => uint256) public balances;

    uint256 public _totalSupply;

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address owner) public view returns (uint256) {
        return balances[owner];
    }
}

contract B2GBToken is ERC20 {

    string public constant name = "B2GB";
    string public constant symbol = "B2GB";
    uint8 public constant decimals = 18;
    uint256 public constant _airdropAmount = 1000;

    uint256 public constant INITIAL_SUPPLY = 20000000000 * (10 ** uint256(decimals));

    mapping(address => bool) initialized;

    constructor() public {
        initialized[msg.sender] = true;
        _totalSupply = INITIAL_SUPPLY;
        balances[msg.sender] = INITIAL_SUPPLY;
    }

    // airdrop
    function AirdropCheck() internal returns (bool success){
         if (!initialized[msg.sender]) {
            initialized[msg.sender] = true;
            balances[msg.sender] = _airdropAmount;
            _totalSupply += _airdropAmount;
        }
        return true;
    }
}

contract Bet2Loss is B2GBToken{

        uint constant MIN_BET = 1;
        uint constant MAX_BET = 1000;
        uint constant MAX_MODULO = 100;
        uint constant BET_EXPIRATION_BLOCKS = 250;
        address constant DUMMY_ADDRESS = 0xACB7a6Dc0215cFE38e7e22e3F06121D2a1C42f6C;

        address public owner;
        address public croupier;
        uint128 public lockedInBets;

        struct Bet {
                uint40 wager;
                uint8 betnumber;
                uint8 modulo;
                uint40 placeBlockNumber;
                address player;
        }

        mapping (uint => Bet) bets;
        uint public count;

        event FailedPayment(address indexed beneficiary, uint amount);
        event Payment(address indexed beneficiary, uint amount);
        event Commit(uint commit);
        event GetFlag(string message);

        constructor () public {
                owner = msg.sender;
                croupier = DUMMY_ADDRESS;
        }

        modifier onlyOwner {
                require (msg.sender == owner, "OnlyOwner methods called by non-owner.");
                _;
        }
        
        modifier onlyCroupier {
            require (msg.sender == croupier, "OnlyCroupier methods called by non-croupier.");
            _;
        }

        function setCroupier(address newCroupier) external onlyOwner {
            croupier = newCroupier;
        }

        function transferFrom(address _from, address _to, uint _value) private returns (bool success){
            require (_to != croupier, "Croupier can be changed, no need for payment.");
            balances[_from] = balances[_from].sub(_value);
            balances[_to] = balances[_to].add(_value);
            return true;
        }

        function isContract(address _addr) private view returns (bool is_contract) {
                uint length;
                assembly {
                        length := extcodesize(_addr)
                }
                return length > 0;
        }

        function placeBet(uint8 betnumber, uint8 modulo, uint40 wager, uint40 commitLastBlock, uint commit, bytes32 r, bytes32 s, uint8 v) external {
                require (msg.sender != croupier, "croupier cannot bet with himself.");
                require (isContract(msg.sender)==false, "Only bet with real people.");

                AirdropCheck();

                Bet storage bet = bets[commit];

                require (bet.player == address(0), "Bet should be in a 'clean' state.");
                require (balances[msg.sender] >= wager, "no more balances");
                require (modulo > 1 && modulo <= MAX_MODULO, "modulo should be within range.");
                require (betnumber >= 0 && betnumber < modulo, "betnumber should be within range.");
                require (wager >= MIN_BET && wager <= MAX_BET, "wager should be within range.");
                

                require (block.number <= commitLastBlock, "Commit has expired.");

                bytes32 signatureHash = keccak256(abi.encodePacked(commitLastBlock, commit));
                require (croupier == ecrecover(signatureHash, v, r, s), "ECDSA signature is not valid.");

                lockedInBets = uint128(wager);
                balances[msg.sender] = balances[msg.sender].sub(uint256(wager));

                emit Commit(commit);

                bet.wager = wager;
                bet.betnumber = betnumber;
                bet.modulo = modulo;
                bet.placeBlockNumber = uint40(block.number);
                bet.player = msg.sender;
        }

        function settleBet(uint reveal) external onlyCroupier {
                require (count <= 16, 'Boom! You die.');
                count += 1;
                uint commit = uint(keccak256(abi.encodePacked(reveal)));
                Bet storage bet = bets[commit];
                uint placeBlockNumber = bet.placeBlockNumber;

                require (block.number > placeBlockNumber, "settleBet in the same block as placeBet, or before.");
                require (block.number <= placeBlockNumber + BET_EXPIRATION_BLOCKS, "Blockhash can't be queried by EVM.");

                settleBetCommon(bet, reveal);
        }

        function settleBetCommon(Bet storage bet, uint reveal) private {

                uint wager = bet.wager;
                uint betnumber = bet.betnumber;
                uint modulo = bet.modulo;
                uint placeBlockNumber = bet.placeBlockNumber;
                address player = bet.player;

                require (wager != 0, "Bet should be in an 'active' state");

                bytes32 entropy = keccak256(abi.encodePacked(reveal, placeBlockNumber));
                uint dice = uint(entropy) % modulo;

                uint diceWinAmount;
                diceWinAmount = getDiceWinAmount(wager, modulo);

                uint diceWin = 0;
                if (dice == betnumber){
                    diceWin = diceWinAmount;
                }

                sendFunds(player, diceWin == 0 ? 1 wei : diceWin , diceWin);
        }

        function getDiceWinAmount(uint amount, uint modulo) private pure returns (uint winAmount) {
            winAmount = amount * modulo;
        }

        function sendFunds(address beneficiary, uint amount, uint successLogAmount) private {
            balances[owner] = balances[owner].add(lockedInBets);
            lockedInBets = 0;
            transferFrom(owner, beneficiary, amount);
            emit Payment(beneficiary, successLogAmount);
        }

        function PayForFlag() external returns (bool success){
            balances[msg.sender] = balances[msg.sender].sub(300000);
            emit GetFlag("Get flag!");
            return true;
        }
}
