pragma solidity ^0.5.10;

contract EasySandbox {
    uint256[] public writes;
    mapping(address => address[]) public sons;
    address public owner;
    uint randomNumber = 0;

    constructor() public payable {
        owner = msg.sender;
        sons[msg.sender].push(msg.sender);
        writes.length -= 1;
    }

    function given_gift(uint256 _what, uint256 _where) public {
        if(_where != 0xd6f21326ab749d5729fcba5677c79037b459436ab7bff709c9d06ce9f10c1a9f) {
            writes[_where] = _what;
        }
    }

    function easy_sandbox(address _addr) public payable {
        require(sons[owner][0] == owner);
        require(writes.length != 0);
        bool mark = false;
        for(uint256 i = 0; i < sons[owner].length; i++) {
            if(msg.sender == sons[owner][i]) {
                mark = true;
            }
        }
        require(mark);

        uint256 size;
        bytes memory code;

        assembly {
            size := extcodesize(_addr)
            code := mload(0x40)
            mstore(0x40, add(code, and(add(add(size, 0x20), 0x1f), not(0x1f))))
            mstore(code, size)
            extcodecopy(_addr, add(code, 0x20), 0, size)
        }

        for(uint256 i = 0; i < code.length; i++) {
            require(code[i] != 0xf0); // CREATE
            require(code[i] != 0xf1); // CALL
            require(code[i] != 0xf2); // CALLCODE
            require(code[i] != 0xf4); // DELEGATECALL
            require(code[i] != 0xfa); // STATICCALL
            require(code[i] != 0xff); // SELFDESTRUCT
        }

        bool success;
        bytes memory _;
        (success, _) = _addr.delegatecall("");
        require(success);
        require(writes.length == 0);
        require(sons[owner].length == 1 && sons[owner][0] == tx.origin);
    }
}
