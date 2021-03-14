pragma solidity ^0.4.21;
contract ZeroLottery {
    struct SeedComponents {
        uint component1;
        uint component2;
        uint component3;
        uint component4;
    }

    uint private base = 8;

    address private owner;
    mapping (address => uint256) public balanceOf;

    function ZeroLottery() public {
        owner = msg.sender;
    }
    
    function init() public payable {
        balanceOf[msg.sender] = 100;
    }

    function seed(SeedComponents components) internal pure returns (uint) {
        uint secretSeed = uint256(keccak256(
            components.component1,
            components.component2,
            components.component3,
            components.component4
        ));
        return secretSeed;
    }
    
    function bet(uint guess) public payable {
        require(msg.value>1 ether);
        require(balanceOf[msg.sender] > 0);
        uint secretSeed = seed(SeedComponents((uint)(block.coinbase), block.difficulty, block.gaslimit, block.timestamp));
        uint n = uint(keccak256(uint(msg.sender), secretSeed)) % base;

        if (guess != n) {
            balanceOf[msg.sender] = 0;
            // charge 0.5 ether for failure
            msg.sender.transfer(msg.value - 0.5 ether);
            return;
        }
        // charge 1 ether for success
        msg.sender.transfer(msg.value - 1 ether);
        balanceOf[msg.sender] = balanceOf[msg.sender] + 100;
    }

    function paolu() public payable {
        require(msg.sender == owner);
        selfdestruct(owner);
    }

}
