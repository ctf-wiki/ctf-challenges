/*
 * The contract deployed on this address is a
 */

pragma solidity =0.4.25;

contract b{
    function Start(string _question, string _answer) public payable;
}
contract a{
    constructor(address t, string q, string r) public{
        b(t).Start(q,r);
    }
}
