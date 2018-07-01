for (int i=0; i<length(provided_flag); i++)
{
	if (main_mapanic(provided_flag[i]) != constant_binary_blob[i])
	{
		bad_boy();
		exit();
	}
	goodboy();
}
