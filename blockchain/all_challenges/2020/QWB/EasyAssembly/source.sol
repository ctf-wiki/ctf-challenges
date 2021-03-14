pragma solidity ^0.5.10;

contract EasyAssembly {
    event SendFlag(address addr);

    uint randomNumber = 0;
    bytes32 private constant ownerslot = keccak256('Welcome to qwb!!! You will find this so easy ~ Happy happy :D');

    bytes32[] public puzzle;
    uint count = 0;
    mapping(address=>bytes32) WinChecksum;
    
    constructor() public payable {
        setAddress(ownerslot, msg.sender);
    }
    
    modifier onlyWin(bytes memory code) {
        require(WinChecksum[msg.sender] != 0);
        bytes32 tmp = keccak256(abi.encodePacked(code));
        address target;
        assembly {
            let t1,t2,t3
            t1 := and(tmp, 0xffffffffffffffff)
            t2 := and(shr(0x40,tmp), 0xffffffffffffffff)
            t3 := and(shr(0x80,tmp), 0xffffffff)
            target := xor(mul(xor(mul(t3, 0x10000000000000000), t2), 0x10000000000000000), t1)
        }
        require(address(target)==msg.sender);
        _;
    }
    
    function setAddress(bytes32 _slot, address _address) internal {
        bytes32 s = _slot;
        assembly { sstore(s, _address) }
    }
    
    function deploy(bytes memory code) internal returns(address addr) {
        assembly {
            addr := create2(0, add(code, 0x20), mload(code), 0x1234)
            if eq(extcodesize(addr), 0) { revert(0, 0) }
        }
    }
    
    function gift() public payable {
        require(count == 0);
        count += 1;
        if(msg.value >= address(this).balance){
            emit SendFlag(msg.sender);
        }else{
            selfdestruct(msg.sender);
        }
    }
    
    function pass(uint idx, bytes memory bytecode) public {
        address addr = deploy(bytecode);
        bytes32 cs = tag(bytecode);
        bytes32 tmp = keccak256(abi.encodePacked(uint(1)));
        uint32 v;
        bool flag = false;

        assembly {
            let v1,v2
            v := sload(add(tmp, idx))
            if gt(v, sload(0)){
                v1 := and(add(and(v,0xffffffff), and(shr(0x20,v), 0xffffffff)), 0xffffffff)
                v2 := and(add(xor(and(shr(0x40,v), 0xffffffff), and(shr(0x60,v), 0xffffffff)), and(shr(0x80,v),0xffffffff)), 0xffffffff)
                if eq(xor(mul(v2,0x100000000), v1), cs){
                    flag := 1                        
                }
            }
        }
        if(flag){
            WinChecksum[addr] = cs;
        }else{
            WinChecksum[addr] = bytes32(0);
        }
    }
    
    function tag(bytes memory a) pure public returns(bytes32 cs) {
        assembly{
            let groupsize := 16
            let head := add(a,groupsize)
            let tail := add(head, mload(a))
            let t1 := 0x13145210
            let t2 := 0x80238023
            let m1,m2,m3,m4,s,tmp
            for { let i := head } lt(i, tail) { i := add(i, groupsize) } {
                s := 0x59129121
                tmp := mload(i)
                m1 := and(tmp,0xffffffff)
                m2 := and(shr(0x20,tmp),0xffffffff)
                m3 := and(shr(0x40,tmp),0xffffffff)
                m4 := and(shr(0x60,tmp),0xffffffff)
                for { let j := 0 } lt(j, 0x4) { j := add(j, 1) } {
                    s := and(mul(s, 2),0xffffffff)
                    t2 := and(add(t1, xor(sub(mul(t1, 0x10), m1),xor(add(t1, s),add(div(t1,0x20), m2)))), 0xffffffff)
                    t1 := and(add(t2, xor(add(mul(t2, 0x10), m3),xor(add(t2, s),sub(div(t2,0x20), m4)))), 0xffffffff)
                }
            }
            cs := xor(mul(t1,0x100000000),t2)
        }
    }
    
    function payforflag(bytes memory code) public onlyWin(code) {
        emit SendFlag(msg.sender);
        selfdestruct(msg.sender);
    }
}
