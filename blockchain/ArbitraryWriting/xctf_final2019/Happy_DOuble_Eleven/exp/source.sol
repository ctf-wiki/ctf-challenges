pragma solidity ^0.4.23;

interface Tmall {
    function Chop_hand(uint) view public returns (bool);
}

contract Happy_DOuble_Eleven {
    
    address public owner;
    bool public have_money;
    bytes32[] public codex;

    bool public have_chopped;
    uint public hand;
    
    mapping (address => uint) public balanceOf;
    mapping (address => uint) public mycart;
    mapping (address => uint) public level;
    
    event pikapika_SendFlag(string b64email);
    
    constructor() public {
        owner = msg.sender;
    }
    
    function payforflag(string b64email) onlyOwner public {
        require(uint(msg.sender) & 0xfff == 0x111);
        require(level[msg.sender] == 3);
        require(mycart[msg.sender] > 10000000000000000000);
        balanceOf[msg.sender] = 0;
        level[msg.sender] = 0;
        have_chopped = false;
        have_money = false;
        codex.length = 0;
        emit pikapika_SendFlag(b64email);
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    
    modifier first() {
        uint x;
        assembly { x := extcodesize(caller) }
        require(x == 0);
        _;
    }
    
    function _transfer(address _from, address _to, uint _value) internal {
        require(_to != address(0x0));
        require(_value > 0);
        
        uint256 oldFromBalance = balanceOf[_from];
        uint256 oldToBalance = balanceOf[_to];
        
        uint256 newFromBalance =  balanceOf[_from] - _value;
        uint256 newToBalance =  balanceOf[_to] + _value;
        
        require(oldFromBalance >= _value);
        require(newToBalance > oldToBalance);
        
        balanceOf[_from] = newFromBalance;
        balanceOf[_to] = newToBalance;
        
        assert((oldFromBalance + oldToBalance) == (newFromBalance + newToBalance));
    }
    
    function transfer(address _to, uint256 _value) public returns (bool success) {
        _transfer(msg.sender, _to, _value); 
        return true;
    }
    
    function Deposit() public payable {
        if(msg.value >= 500 ether){
            mycart[msg.sender] += 1;
        }
    }
    
    function gift() first {
        require(mycart[msg.sender] == 0);
        require(uint(msg.sender) & 0xfff == 0x111);
        balanceOf[msg.sender] = 100;
        mycart[msg.sender] += 1;
        level[msg.sender] += 1;
    }
    
    
    function Chopping(uint _hand) public {
        Tmall tmall = Tmall(msg.sender);
        
        if (!tmall.Chop_hand(_hand)) {
            hand = _hand;
            have_chopped = tmall.Chop_hand(hand);
        }
    }
    function guess(uint num) public {
        uint seed = uint(blockhash(block.number - 1));
        uint rand = seed % 3;
        if (rand == num) {
            have_money = true;
        }
    }
    
    function buy() public {
        require(level[msg.sender] == 1);
        require(mycart[msg.sender] == 1);
        require(have_chopped == true);
        require(have_money == true);
        mycart[msg.sender] += 1;
        level[msg.sender] += 1;
    }
    

    function retract() public {
        require(codex.length == 0);
        require(mycart[msg.sender] == 2);
        require(level[msg.sender] == 2);
        require(have_money == true);
        codex.length -= 1;
    }
    
    function revise(uint i, bytes32 _person) public {
        require(codex.length >= 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000);
        require(mycart[msg.sender] == 2);
        require(level[msg.sender] == 2);
        require(have_money == true);
        codex[i] = _person;
        if (codex.length < 0xffffffffff000000000000000000000000000000000000000000000000000000){
            codex.length = 0;
            revert();
        }
        else{
            level[msg.sender] += 1;
        }
    }
    
    function withdraw(uint _amount) onlyOwner public {
        require(mycart[msg.sender] == 2);
        require(level[msg.sender] == 3);
        require(_amount >= 100);
        require(balanceOf[msg.sender] >= _amount);
        require(address(this).balance >= _amount);
        balanceOf[msg.sender] -= _amount;
        msg.sender.call.value(_amount)();
        mycart[msg.sender] -= 1;
    }
}