pragma solidity ^0.4.24;

contract DaysBank {
    mapping(address => uint) public balanceOf;
    mapping(address => uint) public gift;
    address owner;
        
    constructor()public{
        owner = msg.sender;
    }
    
    event SendFlag(uint256 flagnum, string b64email);
    function payforflag(string b64email) public {
        require(balanceOf[msg.sender] >= 10000);
        emit SendFlag(1,b64email);
    }

    function getgift() public{
        require(gift[msg.sender]==0);
        balanceOf[msg.sender]+=1;
        gift[msg.sender]=1;
    }
    
    function transfer(address towhere, uint howmuch) public {
        require(howmuch>1);
        require(balanceOf[msg.sender]>1);
        require(balanceOf[msg.sender]>=howmuch);
        balanceOf[msg.sender]-=howmuch;
        balanceOf[towhere]+=howmuch;
    }
    
    function profit() public{
        require(balanceOf[msg.sender]==1);
        require(gift[msg.sender]==1);
        balanceOf[msg.sender]+=1;
        gift[msg.sender]=2;
    }
    
    function transfer2(address towhere, uint howmuch) public {
        require(howmuch>2);
        require(balanceOf[msg.sender]>2);
        require(balanceOf[msg.sender]-howmuch>0);
        balanceOf[msg.sender]-=howmuch;
        balanceOf[towhere]+=howmuch;
    }
}
