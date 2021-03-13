pragma solidity ^0.5.10;

contract CreativityPlus {
    event SendFlag(address addr);
    
    address public target;
    address public owner;
    uint randomNumber = RN;
    
    constructor() public {
        owner = msg.sender;
    }
    
    modifier onlyOwner(){
        require(msg.sender == owner);
        _;
    }
    
    function check(address _addr) public {
        uint size;
        assembly { size := extcodesize(_addr) }
        require(size > 0 && size <= 4);
        target = _addr;
    }
    
    function execute() public {
        require( target != address(0) );
        address tmp;
        uint size;
        assembly { 
            tmp := and(sload(0),0xffffffffffffffffffffffffffffffffffffffff)
            size := extcodesize(tmp) 
        }
        require( size > 0 && size <= 10);
        (bool flag, ) = tmp.call(abi.encodeWithSignature(""));
        if(flag == true) {
            owner = msg.sender;
        }
    }
    
    function payforflag() public payable onlyOwner {
        emit SendFlag(msg.sender);
        selfdestruct(msg.sender);
    }
}

