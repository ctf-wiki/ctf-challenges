pragma solidity ^0.4.23;

contract FakeOwnerGame {
    event SendFlag(address _addr);
    
    uint randomNumber = 0;
    uint time = now;
    mapping (address => uint) public BalanceOf;
    mapping (address => uint) public WinCount;
    mapping (address => uint) public FailCount;
    bytes32[] public codex;
    address private owner;
    uint256 settlementBlockNumber;
    address guesser;
    uint8 guess;
    
    struct FailedLog {
        uint failtag;
        uint failtime;
        uint success_count;
        address origin;
        uint fail_count;
        bytes12 hash;
        address msgsender;
    }
    mapping(address => FailedLog[]) FailedLogs;
    
    constructor() {
        owner = msg.sender;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    
    function payforflag() onlyOwner {
        require(BalanceOf[msg.sender] >= 2000);
        emit SendFlag(msg.sender);
        selfdestruct(msg.sender);
    }
    
    function lockInGuess(uint8 n) public payable {
        require(guesser == 0);
        require(msg.value == 1 ether);

        guesser = msg.sender;
        guess = n;
        settlementBlockNumber = block.number + 1;
    }
    
    function settle() public {
        require(msg.sender == guesser);
        require(block.number > settlementBlockNumber);

        uint8 answer = uint8(keccak256(block.blockhash(block.number - 1), now)) % 2;

        if (guess == answer) {
            WinCount[msg.sender] += 1;
            BalanceOf[msg.sender] += 1000;
        } else {
            FailCount[msg.sender] += 1;
        }
        
        if (WinCount[msg.sender] == 2) {
            if (WinCount[msg.sender] + FailCount[msg.sender] <= 2) {
                guesser = 0;
                WinCount[msg.sender] = 0;
                FailCount[msg.sender] = 0;
                msg.sender.transfer(address(this).balance);
            } else {
                FailedLog failedlog;
                failedlog.failtag = 1;
                failedlog.failtime = now;
                failedlog.success_count = WinCount[msg.sender];
                failedlog.origin = tx.origin;
                failedlog.fail_count = FailCount[msg.sender];
                failedlog.hash = bytes12(sha3(WinCount[msg.sender] + FailCount[msg.sender]));
                failedlog.msgsender = msg.sender;
                FailedLogs[msg.sender].push(failedlog);
            }
        }
    }

    function beOwner() payable {
        require(address(this).balance > 0);
        if(msg.value >= address(this).balance){
            owner = msg.sender;
        }
    }
    
    function revise(uint idx, bytes32 tmp) {
        codex[idx] = tmp;
    }
}
