pragma solidity ^0.4.23;

contract babybank {
    mapping(address => uint) public balance;
    mapping(address => uint) public level;
    address owner;
    uint secret;
    
    //Don't leak your teamtoken plaintext!!! md5(teamtoken).hexdigest() is enough.
    //Gmail is ok. 163 and qq may have some problems.
    event sendflag(string md5ofteamtoken,string b64email); 
    
    
    constructor()public{
        owner = msg.sender;
    }
    
    //pay for flag
    function payforflag(string md5ofteamtoken,string b64email) public{
        require(balance[msg.sender] >= 10000000000);
        balance[msg.sender]=0;
        owner.transfer(address(this).balance);
        emit sendflag(md5ofteamtoken,b64email);
    }
    
    modifier onlyOwner(){
        require(msg.sender == owner);
        _;
    }
    
    //challenge 1 
    function profit() public{
        require(level[msg.sender]==0);
        require(uint(msg.sender) & 0xffff==0xb1b1);
        balance[msg.sender]+=1;
        level[msg.sender]+=1;
    }
    
    //challenge 2
    function set_secret(uint new_secret) public onlyOwner{
        secret=new_secret;
    }
    function guess(uint guess_secret) public{
        require(guess_secret==secret);
        require(level[msg.sender]==1);
        balance[msg.sender]+=1;
        level[msg.sender]+=1;
    }
    
    //challenge 3
    
    function transfer(address to, uint amount) public{
        require(balance[msg.sender] >= amount);
        require(amount==2);
        require(level[msg.sender]==2);
        balance[msg.sender] = 0;
        balance[to] = amount;
    }
    
    function withdraw(uint amount) public{
        require(amount==2);
        require(balance[msg.sender] >= amount);
        msg.sender.call.value(amount*100000000000000)();
        balance[msg.sender] -= amount;
    }
}
