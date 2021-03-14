pragma solidity ^0.5.10;

contract Creativity {
    event SendFlag(address addr);
    
    address public target;
    uint randomNumber = RN;
    
    function check(address _addr) public {
        uint size;
        assembly { size := extcodesize(_addr) }
        require(size > 0 && size <= 4);
        target = _addr;
    }
    
    function execute() public {
        require(target != address(0));
        target.delegatecall(abi.encodeWithSignature(""));
        selfdestruct(address(0));
    }
    
    function sendFlag() public payable {
        require(msg.value >= 100000000 ether);
        emit SendFlag(msg.sender);
    }
}
