/**
 *Submitted for verification at Etherscan.io on 2019-12-06
*/

pragma solidity ^0.5.11;

contract Montagy{
    address payable public owner;
    mapping(bytes32=>bool) isOfficialChecksum;
    mapping(address=>bytes32) puzzleChecksum;
    address public lastchildaddr;
    string public winnerinfo;
    bool public _gameon;
    constructor() public payable{
        owner = msg.sender;
        _gameon = false;
    }
    modifier onlyOwner(){
        require(msg.sender == owner);
        _;
    }
    modifier onlyPuzzle(){
        require(puzzleChecksum[msg.sender] != 0);
        _;
    }
    modifier onlyGameOn(){
        require(_gameon);
        _;
    }
    
    function read_slot(uint k) public view returns (bytes32 res) {
        assembly { res := sload(k) }
    }

    function cal_addr(uint k, uint p) public pure returns(bytes32 res) {
        res = keccak256(abi.encodePacked(k, p));
    }
    
    function cal_addr(uint p) public pure returns(bytes32 res) {
        res = keccak256(abi.encodePacked(p));
    }
    
    
    function setGame(bool status) public onlyOwner{
        _gameon = status;
    }
    
    function registerCode(bytes memory a) public onlyOwner {
        isOfficialChecksum[tag(a)]=true;
    }
    
    function newPuzzle(bytes memory code) public onlyGameOn returns(address addr){
        bytes32 cs = tag(code);
        require(isOfficialChecksum[cs]);
        
        addr = deploy(code);
        lastchildaddr=addr;
        puzzleChecksum[addr] = cs;
    }
    
    function solve(string memory info) public onlyGameOn onlyPuzzle {
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
                for { let j := 0 } lt(j, 0x4) { j := add(j, 1) } {
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

contract P3 {
    Montagy public server;
    constructor() public {
        server = Montagy(0xd95C819d1DFBD085dFf0b3351230958Cb6075957);
    }
    function do_solve() public {
        server.solve('balsn');
    }
}
