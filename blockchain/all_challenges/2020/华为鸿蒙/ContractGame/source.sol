pragma solidity ^0.4.23;

contract ContractGame {
    
    event SendFlag(address addr);
    
    mapping(address => bool) internal authPlayer;
    uint private blocknumber;
    uint private gameFunds;
    uint private cost;
    bool private gameStopped = false;
    address public owner;
    bytes4 private winningTicket;
    uint randomNumber = 0;
    mapping(address=>bool) private potentialWinner;
    mapping(address=>uint256) private rewards;
    mapping(address=>bytes4) private ticketNumbers;
    
    constructor() public payable {
        gameFunds = add(gameFunds, msg.value);
        cost = div(gameFunds, 10);
        owner = msg.sender;
        rewards[address(this)] = msg.value;
    }
    
    modifier auth() {
        require(authPlayer[msg.sender], "you are not authorized!");
        _;
    }
    
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");

        return c;
    }
    
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a);
        uint256 c = a - b;
        return c;
    }
    
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        require(c / a == b, "SafeMath: multiplication overflow");
        return c;
    }
    
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b > 0);
        uint256 c = a / b;
        return c;
    }
    
    function BetGame(bool mark) external payable {
        require(msg.value == cost);
        require(gameFunds >= div(cost, 2));
        bytes32 entropy = blockhash(block.number-1);
        bytes1 coinFlip = entropy[10] & 1;
        if ((coinFlip == 1 && mark) || (coinFlip == 0 && !mark)) {
            gameFunds = sub(gameFunds, div(msg.value, 2));
            msg.sender.transfer(div(mul(msg.value, 3), 2));
        } else {
            gameFunds = add(gameFunds, msg.value);
        }
        
        if (address(this).balance==0) {
            winningTicket = bytes4(0);
            blocknumber = block.number + 1;
            gameStopped = false;
            potentialWinner[msg.sender] = true;
            rewards[msg.sender] += msg.value;
            ticketNumbers[msg.sender] = bytes4((msg.value - cost)/10**8);
        }
    }
    
    function closeGame() external auth {
        require(!gameStopped);
        require(blocknumber != 0);
        require(winningTicket == bytes4(0));
        require(block.number > blocknumber);
        require(msg.sender == owner || rewards[msg.sender] > 0);
        winningTicket = bytes4(blockhash(blocknumber));
        potentialWinner[msg.sender] = false;
        gameStopped = true;
    }
    
    function winGame() external auth {
        require(gameStopped);
        require(potentialWinner[msg.sender]);
        if(winningTicket == ticketNumbers[msg.sender]){
            emit SendFlag(msg.sender);
        }
        selfdestruct(msg.sender);
    }
    
    function AddAuth(address addr) external {
        authPlayer[addr] = true;
    }
    
    function() public payable auth{
        if(msg.value == 0) {
            this.closeGame();
        } else {
            this.winGame();
        }
    }
}
