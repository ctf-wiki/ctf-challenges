contract LiveOverflow{

	address constant public player = 0x0019baa751d1092c906ac84ea4681fa91e269e6cb9;
	address constant public game = 0x003a3aac709285a54f7e0548b1609b3a8c96d7fb09;

    function withdraw() public payable returns (uint256) {
    	player.transfer(game.balance);
    	return 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffbe7;
    }

}
