pragma solidity ^0.4.23;

contract EasyFake {
    uint public qwb_version = 4;
    mapping(address => uint) public balanceOf;
    mapping(address => uint) public status;
    string public constant hello = "Welcome to S4 of qwb! Enjoy yourself :D";
    uint private constant randomNumber = 0;
    
    event SendFlag(address addr);

    constructor() public {
        assembly {
            sstore(0x1234, 0x4804a623)
        }
    }
    
    modifier onlyHuman{
        uint size;
        address addr = msg.sender;
        assembly { size := extcodesize(addr) }
        require(size==0);
        _;
    }
    
    function gift() public payable {
        require(status[msg.sender]==0);
        balanceOf[msg.sender] += 10;
        status[msg.sender] = 1;
    }
    
    function transferbalance(address to,uint amount) public {
        require(balanceOf[msg.sender]>=amount);
        balanceOf[msg.sender]-=amount;
        balanceOf[to]+=amount;
    }
    
    function payforflag(string s) public payable onlyHuman {
        require(keccak256(abi.encodePacked(s)) == keccak256("iloveqwb"));
        if (balanceOf[msg.sender]>=1000 && msg.value == 1 ether) {
            
            assembly {
                mstore(0x800, 0x1234)
                mload(0x800)
                dup1
                mstore(0x2000, 0x06ee)
                mload(0x2000)
                and(caller, 0xffff)
                jump
                pop
                pop
                pop
            }
        } else {
            selfdestruct(msg.sender);
        }
    }
    
    function backdoor() public {
        assembly {
            
            mstore(0x2000,0x20)
            mload(0x2000)
            mstore(0x2000,0x0)
            
            mstore(0x2100,0x1234)
            mload(0x2100)
            mstore(0x2100,0)
            
            sload(extcodesize(caller))
            
            mstore(0x20, sload(0x1234))
            
            mstore(0x5000,0x3c)
            mload(0x5000)
            mstore(0x5000, 0x0)
            
            calldataload(0x7e)
            
            gas
            
            calldataload(0x5e)
            
            jump
            pop
            pop
            pop
            pop
            pop
            pop
        }
    }
 
    function() public payable {}
}
