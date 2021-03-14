pragma solidity ^0.5.11;

contract Montagy{
    function solve(string memory info) public;
}
contract Puzzle{
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
