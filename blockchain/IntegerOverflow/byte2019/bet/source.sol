pragma solidity ^0.4.24;

contract bet {
    uint secret;
    address owner;
    
    mapping(address => uint) public balanceOf;
    mapping(address => uint) public gift;
    mapping(address => uint) public isbet;
    
    event SendFlag(string b64email);
    
    function Bet() public{
        owner = msg.sender;
    }
    
    function payforflag(string b64email) public {
        require(balanceOf[msg.sender] >= 100000);
        balanceOf[msg.sender]=0;
        owner.transfer(address(this).balance);
        emit SendFlag(b64email);
    }
    

    //to fuck
    
    modifier only_owner() {
        require(msg.sender == owner);
        _;
    }
    
    function setsecret(uint secretrcv) only_owner {
        secret=secretrcv;
    }
    
    function deposit() payable{
        uint geteth=msg.value/1000000000000000000;
        balanceOf[msg.sender]+=geteth;
    }
    
    function profit() {
        require(gift[msg.sender]==0);
        gift[msg.sender]=1;
        balanceOf[msg.sender]+=1;
    }
    
    function betgame(uint secretguess){
        require(balanceOf[msg.sender]>0);
        balanceOf[msg.sender]-=1;
        if (secretguess==secret)
        {
            balanceOf[msg.sender]+=2;
            isbet[msg.sender]=1;
        }
    }
    
    function doublebetgame(uint secretguess) only_owner{
        require(balanceOf[msg.sender]-2>0);
        require(isbet[msg.sender]==1);
        balanceOf[msg.sender]-=2;
        if (secretguess==secret)
        {
            balanceOf[msg.sender]+=2;
        }
    }

}
