pragma solidity ^0.5.10;

contract BoxGame {

    event ForFlag(address addr);
    address public target;
    
    constructor(bytes memory a) payable public {
        assembly {
            return(add(0x20, a), mload(a))
        }
    }
    
    function check(address _addr) public {
        uint size;
        assembly { size := extcodesize(_addr) }
        require(size > 0 && size <= 4);
        target = _addr;
    }
    
    function payforflag(address payable _addr) public {
        
        require(_addr != address(0));
        
        target.delegatecall(abi.encodeWithSignature(""));
        selfdestruct(_addr);
    }
    
    function sendFlag() public payable {
        require(msg.value >= 1000000000 ether);
        emit ForFlag(msg.sender);
    }

}
