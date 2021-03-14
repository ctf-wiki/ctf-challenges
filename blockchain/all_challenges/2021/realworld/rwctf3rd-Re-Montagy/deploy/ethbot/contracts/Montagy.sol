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

contract P2{
    Montagy public server;
    constructor() public{
        server = Montagy(msg.sender);
    }
    uint256 a;
    uint256 b;
    uint256 c;
    uint256 d;
    uint256 e;
    uint256 f;
    uint256 g;
    uint256 h;
    uint256 i;
    function monica_init(uint256 _a, uint256 _b, uint256 _c, uint256 _d, uint256 _e, uint256 _f, uint256 _g, uint256 _h, uint256 _i) public {
        a=_a;
        b=_b;
        c=_c;
        d=_d;
        e=_e;
        f=_f;
        g=_g;
        h=_h;
        i=_i;
    }
    function loose() view public returns(bool){
        uint256 t1 = (a^b^c)+(d^e^f)+(g^h^i);
        uint256 t2 = (a+d+g)^(b+e+h)^(c+f+i);
        require(t1 + t2 < 0xaabbccdd);
        require(t1 > 0x8261e26b90505061031256e5afb60721cb);
        require(0xf35b6080614321368282376084810151606401816080016143855161051756 >= t1*t2);
        require(t1 - t2 >= 0x65e670d9bd540cea22fdab97e36840e2);
        return true;
    }
    function harsh(bytes memory seed, string memory info) public{
        require(loose());
        if (keccak256(seed) == bytes32(bytes18(0x6111d850336107ef16565b908018915a9056))) {
            server.solve(info);
        }
    }

}