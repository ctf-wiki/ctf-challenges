pragma solidity ^0.4.25;

library MathLib {
    function toBytes(uint256 x) internal returns (bytes b) {
        b = new bytes(32);
        assembly { mstore(add(b, 32), x) }
    }
    
    function B2I(bytes x) internal returns (uint256 b) {
        assembly { 
            b := mload(add(x, 0x20))
        }
    }
    
    function encrypt(bytes _base) internal returns (bytes) {
        bytes memory N1 = hex"968da1c57dbcb8ccd629697e55d998ae9d8f5082936c5c95ee30932af4acaa79";
        bytes memory e = hex"010001";
        return modexp(_base, e, N1);
    }
    
    function encrypt2(uint _base) internal returns (uint) {
        uint N1 = 68097169229136709291059559437094840645334043223665783465588958281537866738297;
        return _base ^ N1;
    }
    
    function modexp(bytes memory _base, bytes memory _exp, bytes memory _mod) internal view returns(bytes memory ret) {
        assembly {
            let bl := mload(_base)
            let el := mload(_exp)
            let ml := mload(_mod)
            let freemem := mload(0x40) 
            mstore(freemem, bl)        
            mstore(add(freemem,32), el) 
            mstore(add(freemem,64), ml) 
            let success := staticcall(450, 0x4, add(_base,32), bl, add(freemem,96), bl)
            let size := add(96, bl)
            success := staticcall(450, 0x4, add(_exp,32), el, add(freemem,size), el)
            size := add(size,el)
            success := staticcall(450, 0x4, add(_mod,32), ml, add(freemem,size), ml)
            switch success case 0 { invalid() }
            size := add(size,ml)
            success := staticcall(sub(gas, 1350), 0x5, freemem, size, add(96,freemem), ml)
            switch success case 0 { invalid() }
            let length := ml
            let length_ptr := add(96,freemem)
            for { } eq ( eq(mload(length_ptr), 0), 1) { } {
               length_ptr := add(length_ptr, 0x20)        
               length := sub(length,0x20) 
            } 
            ret := sub(length_ptr,0x20)
            mstore(ret, length)
            mstore(0x40, add(add(96, freemem),ml))
        }        
    }
}

contract AttackConstract {
    uint public rvalue;
    address owner;
    function AttackConstract(address _owner, uint _value) { rvalue = _value; owner = _owner;}
    function () payable { selfdestruct(owner); }
}

contract HCTF2018User {
    string banner;
    using MathLib for *;
    
    function HCTF2018User() {
        banner = "Welcome to HCTF 2018 ethereum smart contract challenge!";
    }
    
    function setkey(uint256 _value, uint256 _addr) public payable {
        require(msg.value >= 1 ether, "poor people!!");
        address target = address(_value);
        AttackConstract other = AttackConstract(target);
        uint256 rvalue = other.rvalue() + (block.number * msg.value);
        target.transfer(msg.value);
        require(target.balance == 0, "you can't get money from me!");
        uint256 result = MathLib.B2I(MathLib.encrypt(MathLib.toBytes(_value)));
        uint256 radd = MathLib.B2I(MathLib.encrypt(MathLib.toBytes(_addr)));
        uint256 new_radd = radd ^ result;
        require(new_radd != 0);
        require(new_radd != 1);
        setstore(new_radd, rvalue);
    }
    
    function setstore(uint256 _key, uint256 _value) private {
        assembly {
            sstore(_key, _value)
        }
    }
    function getstore(uint256 _key) external returns (uint256 _value) {
        assembly {
            _value := sload(_key)
        }
    }
    
    function win_money() public {
        address admin = 0x020f5b6059a58154b861943ecf07e92f6d458575;
        admin.transfer(this.balance);
    }
    
    function () payable {}

}

contract HCTF2018Admin {
    string banner;
    address owner;
    HCTF2018User users;
    
    function HCTF2018Admin(address _owner, address User) {
        banner = "Only admin can execute this contract!";
        owner = _owner;
        users = HCTF2018User(User);
    }
    function getflag(uint256 tokenhash) public constant returns (bool) {
        require(msg.sender == owner, "Only Owner can call getflag function!");
        uint256[2] memory G;
        G[0] = 55066263022277343669578718895168534326250603453777594175500187360389116729240;
        G[1] = 32670510020758816978083085130507043184471273380659243275938904335757337482424;
        uint256 addr = ecmulVerify(G[0], G[1], tokenhash);
        // bytes memory salt = hex"23e15a398316570c9f5eb8c757c57c7131f79497e7e5b17b011969f175e424fd";
        uint256 right = users.getstore(addr);
        if (right + addr < right)
            return true;
        else
            return false;
    }
    function ecmulVerify(uint256 x1, uint256 y1, uint256 scalar) private pure returns(uint256)
    {
        uint256 m = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141;
        address signer = ecrecover(0, y1 % 2 != 0 ? 28 : 27, bytes32(x1), bytes32(mulmod(scalar, x1, m)));
        return uint256(signer);
    }
}


contract createContract {
    string banner;
    address owner;
    using MathLib for *;
    function createContract(address _owner) payable {
        banner = "You don't know anything about power!!!Welcome to HCTF 2018";
        owner = _owner;
        new HCTF2018User();
    }
    
    function addContract(uint[] _data) public {
        require(msg.sender == owner, "Only admin can execute this function!");
        for (uint i=0; i < _data.length; i++) {
            _data[i] = MathLib.encrypt2(_data[i]);
        }
        assembly {
            let addr := create(callvalue, add(_data, 0x20), mul(0x20,mload(_data)))
        }
    }
}
