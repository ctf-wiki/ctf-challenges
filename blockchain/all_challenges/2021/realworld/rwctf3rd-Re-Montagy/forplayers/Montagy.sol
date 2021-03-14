pragma solidity ^0.5.11;

contract Montagy{
    address payable public owner;
    mapping(bytes32=>uint256) registeredIDLength;
    mapping(address=>bytes32) puzzleID;
    address public lastchildaddr;
    string public winnerinfo;
    constructor() public payable{
        owner = msg.sender;
    }
    modifier onlyOwner(){
        require(msg.sender == owner);
        _;
    }
    modifier onlyPuzzle(){
        require(puzzleID[msg.sender] != 0);
        _;
    }

    function registerCode(bytes memory a) public onlyOwner {
        registeredIDLength[tag(a)] = a.length;
    }

    function newPuzzle(bytes memory code) public returns(address addr){
        bytes32 id = tag(code);
        require(registeredIDLength[id] == code.length);

        addr = deploy(code);
        lastchildaddr = addr;
        puzzleID[addr] = id;
    }

    function solve(string memory info) public onlyPuzzle {
        owner.transfer(address(this).balance);
        winnerinfo = info;
    }

    function deploy(bytes memory code) private returns(address addr){
        assembly {
            addr := create(0,add(code,0x20), mload(code))
            if eq(extcodesize(addr), 0) { revert(0, 0) }
        }
    }

    function tag(bytes memory a) pure public returns(bytes32 cs){
        assembly{
            let groupsize := 16
            let head := add(a,groupsize)
            let tail := add(head, mload(a))
            let t1 := 0x21711730
            let t2 := 0x7312f103
            let m1,m2,m3,m4,p1,p2,p3,s,tmp
            for { let i := head } lt(i, tail) { i := add(i, groupsize) } {
                s := 0x6644498b
                tmp := mload(i)
                m1 := and(tmp,0xffffffff)
                m2 := and(shr(0x20,tmp),0xffffffff)
                m3 := and(shr(0x40,tmp),0xffffffff)
                m4 := and(shr(0x60,tmp),0xffffffff)
                for { let j := 0 } lt(j, 0x10) { j := add(j, 1) } {
                    s := and(add(s, 0x68696e74),0xffffffff)
                    p1 := sub(mul(t1, 0x10), m1)
                    p2 := add(t1, s)
                    p3 := add(div(t1,0x20), m2)
                    t2 := and(add(t2, xor(p1,xor(p2,p3))), 0xffffffff)
                    p1 := add(mul(t2, 0x10), m3)
                    p2 := add(t2, s)
                    p3 := sub(div(t2,0x20), m4)
                    t1 := and(add(t1, xor(p1,xor(p2,p3))), 0xffffffff)
                }
            }
            cs := xor(mul(t1,0x100000000),t2)
        }
    }
}
