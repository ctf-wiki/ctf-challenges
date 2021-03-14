pragma solidity ^0.4.23;

contract StrictMathematician {
    address owner;
    string private constant welcome = "Oh, fantansitic baby! I am a strict mathematician";
    uint randomNumber = 0;
    uint createtime = now;
    
    constructor() public payable{
        owner = msg.sender;
    }
    
    struct Target {
        function() internal callback;
        uint32 value;
        address origin;
        address sender;
        bytes12 hash;
        uint time;
    }
    Target[] Targets;
    
    struct FailLog {
        uint idx;
        address origin;
        uint time;
        bytes12 guessnum;
        address sender;
    }
    mapping(address => FailLog[]) FailLogs;
    event SendFlag(address addr);
    
    function start(bytes12 hash) public payable {
        Target target;
        target.origin = tx.origin;
        target.sender = msg.sender;
        target.hash = hash;
        require(msg.value == 1 ether);
        target.value += 1;
        Targets.push(target);
    }
    
    function guess(uint idx, bytes12 num) public {
        if (bytes12(keccak256(abi.encodePacked(num))) != Targets[idx].hash) {
            FailLog faillog;
            faillog.idx = idx;
            faillog.time = now;
            faillog.origin = tx.origin;
            faillog.sender = msg.sender;
            faillog.guessnum = num;
            FailLogs[msg.sender].push(faillog);
        } else {
            Target target = Targets[idx];
            target.value += 1;
        }
    }
    
    function check(uint idx, uint tmp) public {
        uint maxlen = check_len(address(msg.sender)) + tmp * 3 / 4 ;
        require(uint(read_slot(uint(cal_mapaddr(uint(msg.sender),4)))) <= maxlen);
        require(tmp != 0);
        Target target = Targets[idx+tmp];
        require(uint32(target.value+1)==0);
        target.callback();
    }
    
    function payforflag() public payable {
        require(address(this).balance == 0);
        emit SendFlag(msg.sender);
        selfdestruct(msg.sender);
    }
    
    function read_slot(uint k) internal view returns (bytes32 res) {
        assembly { res := sload(k) }
    }

    function cal_mapaddr(uint k, uint p) internal pure returns(bytes32 res) {
        res = keccak256(abi.encodePacked(k, p));
    }
    
    function cal_arrayaddr(uint p) internal pure returns(bytes32 res) {
        res = keccak256(abi.encodePacked(p));
    }
    
    function check_len(address addr) internal pure returns(uint maxlen){

        uint res = uint(cal_arrayaddr(uint(cal_mapaddr(uint(addr),4))));
        uint sum = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff;
        uint begin = uint(keccak256(abi.encodePacked(uint(3))));
        uint distance;
        uint remainder;
        
        if (res>begin) {
            distance = res - begin;
        } else{
            distance = sum - begin + res + 1;
        }
        
        remainder = distance % 3;
        if (remainder==0) {
            maxlen = 1;
        } else if (remainder==1) {
            maxlen = 3;
        } else {
            maxlen = 2;
        }
    }
}
