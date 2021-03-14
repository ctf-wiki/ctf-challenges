pragma solidity ^0.6.12;

contract EthEnc {
    address private owner;    //0
    
    uint private key;        //1
    
    uint private delta;     //2
    
    uint public output;       //3
    
    uint32 private sum;
    uint224 private tmp_sum=0; //4
    
    uint32 private key0;
    uint224 private t0=0;  //5
    uint32 private key1;
    uint224  private t1=0;  //6
    uint32 private key2;
    uint224 private  t2=0;  //7
    uint32  private key3;
    uint224 private  t3=0;  //8
    uint randomNumber = 0;
    string private s;
    
    event OhSendFlag(address addr);
    
    constructor() public payable {
        // key = 0x74686974 5f69735e 5f746573 746b6579
        key = 0x746869745f69735e5f746573746b6579;
        delta = 0xb3c6ef3720;
    }
    
    modifier auth {
        require(msg.sender == owner || msg.sender == address(this), "EthEnc: not authorized");
        _;
    }
    
    function payforflag() public auth {
        require(output == 2282910687825444608285583946662268071674116917685196567156);
        emit OhSendFlag(msg.sender);
        selfdestruct(msg.sender);
    }
    
    function Convert(string memory source) internal pure returns (uint result) {
        bytes32 tmp;
        assembly {
            tmp := mload(add(source, 32))
        }
        result = uint(tmp) / 0x10000000000000000;
    }
    
    // 正 0x 5f5f6f68 5f66616e 74616e73 69746963 5f626162 795f5f5f __oh_fantansitic_baby___
    
    function set_s(string memory _s) public {
        s = _s;
    }
    
    function Encrypt() public {
        uint tmp = Convert(s);
        assembly {
            let first,second
            sstore(5, and(shr(96, sload(1)), 0xffffffff))
            sstore(6, and(shr(64, sload(1)), 0xffffffff))
            sstore(7, and(shr(32, sload(1)), 0xffffffff))
            sstore(8, and(sload(1), 0xffffffff))
            
            let step := 1
            for { let i := 1 } lt(i, 4) { i := add(i, 1) } {
                
                first := and(shr(mul(add(sub(24, mul(i, 8)), 4), 8), tmp), 0xffffffff)
                second := and(shr(mul(sub(24, mul(i, 8)), 8), tmp), 0xffffffff)
                
                sstore(4, 0)
                
                for {let j := 0 } lt(j, 32) { j := add(j, 1) } {
                    
                    let tmp11,tmp12
                    let tmp21,tmp22
                    
                    tmp11 := and(add(xor(and(mul(second, 16), 0xffffffff), and(div(second, 32), 0xffffffff)), second), 0xffffffff)
                    switch and(and(sload(4),0xffffffff), 3)
                    case 0 {
                        tmp12 := and(add(and(sload(4),0xffffffff), and(sload(5),0xffffffff)), 0xffffffff)
                    }
                    case 1 {
                        tmp12 := and(add(and(sload(4),0xffffffff), and(sload(6),0xffffffff)), 0xffffffff)
                    }
                    case 2 {
                        tmp12 := and(add(and(sload(4),0xffffffff), and(sload(7),0xffffffff)), 0xffffffff)
                    }
                    default {
                        tmp12 := and(add(and(sload(4),0xffffffff), and(sload(8),0xffffffff)), 0xffffffff)
                    }
                    first := and(add(first, xor(tmp11, tmp12)), 0xffffffff)
                    
                    sstore(4, and(add(and(sload(4), 0xffffffff), shr(5, sload(2))), 0xffffffff))
                    
                    tmp21 := and(add(xor(and(mul(first, 16), 0xffffffff), and(div(first, 32), 0xffffffff)), first), 0xffffffff)
                    switch and(and(shr(11, and(sload(4),0xffffffff)), 0xffffffff), 3)
                    case 0 {
                        tmp22 := and(add(and(sload(4),0xffffffff), and(sload(5),0xffffffff)), 0xffffffff)
                    }
                    case 1 {
                        tmp22 := and(add(and(sload(4),0xffffffff), and(sload(6),0xffffffff)), 0xffffffff)
                    }
                    case 2 {
                        tmp22 := and(add(and(sload(4),0xffffffff), and(sload(7),0xffffffff)), 0xffffffff)
                    }
                    default {
                        tmp22 := and(add(and(sload(4),0xffffffff), and(sload(8),0xffffffff)), 0xffffffff)
                    }
                    second := and(add(second, xor(tmp21, tmp22)), 0xffffffff)

                }
                
                sstore(3, add(sload(3), add(shl(sub(192, mul(step, 32)), first), shl(sub(192, mul(i, 64)), second))))
                step := add(step, 2)
            }
        }
    }
    
    receive() external payable {
        if(msg.value == 0) {
            this.payforflag();
        } else {
            this.Encrypt();
        }
    }
}
