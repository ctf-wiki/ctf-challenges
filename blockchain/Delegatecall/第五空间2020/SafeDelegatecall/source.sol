pragma solidity ^0.4.23;

contract SafeDelegatecall {
    
    address private owner;
    bytes4 internal constant SET = bytes4(keccak256('fifth(uint256)'));
    event SendFlag(address addr);
    uint randomNumber = RN;
    
    struct Func {
        function() internal f;
    }
    
    constructor() public payable {
        owner = msg.sender;
    }
    
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    
    function execute(address _target) public payable{
        require(_target.delegatecall(abi.encodeWithSelector(this.execute.selector)) == false, 'unsafe execution');
        
        bytes4 sel; 
        uint val;
        
        (sel, val) = getRet();
        require(sel == SET);
        
        Func memory func;
        func.f = gift;
        assembly { 
            mstore(func, sub(mload(func), val))
        }
        func.f();
    }
    
    function gift() private {
        payforflag();
    }
    
    function getRet() internal pure returns (bytes4 sel, uint val) {
        assembly {
            if iszero(eq(returndatasize, 0x24)) { revert(0, 0) }
            let ptr := mload(0x40)
            returndatacopy(ptr, 0, 0x24)
            sel := and(mload(ptr), 0xffffffff00000000000000000000000000000000000000000000000000000000)
            val := mload(add(0x04, ptr))
        }
    }
    
    function payforflag() public payable onlyOwner {
        require(msg.value == 1, 'I only need a little money!');
        emit SendFlag(msg.sender);
        selfdestruct(msg.sender);
    }
    
    function() payable public{}
}

