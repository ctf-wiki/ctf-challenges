import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.List;

public class Verify {

    class AnonymousClass1 implements MapAction<String, byte[]> {
        private final /* synthetic */ String val$password;

        AnonymousClass1(String str) {
            this.val$password = str;
        }

        public byte[] action(String element) {
            try {
                MessageDigest digest = MessageDigest.getInstance(element);
                digest.update(this.val$password.getBytes());
                return digest.digest();
            } catch (NoSuchAlgorithmException e) {
                return null;
            }
        }
    }
	public static void main(String argv[]){
		for(int i=0;i<9999999;++i){
			String s = String.format("%d", i)
			String tmp = isOk(s);
			if (s.equals("be790d865f2cea9645b3f79c0342df7e")) {
				System.out.println("FOUND!! " + s);
				return;
			}
		}
	}
	# remove the argument c
    public static String isOk(String _password) {
        String password = _password;
        if (_password.length() > 7) {
            password = _password.substring(0, 7);
        }
        return OneWayFunction(password);
    }

    private static String OneWayFunction(String password) {
        List<byte[]> bytes = ArrayTools.map(ArrayTools.select(ArrayTools.map(new String[]{"MD2", "MD5", "SHA-1", "SHA-256", "SHA-384", "SHA-512"}, new AnonymousClass1(password)), new SelectAction<byte[]>() {
            public boolean action(byte[] element) {
                return element != null;
            }
        }), new MapAction<byte[], byte[]>() {
            public byte[] action(byte[] element) {
                int i;
                byte[] b = new byte[8];
                for (i = 0; i < b.length / 2; i++) {
                    b[i] = element[i];
                }
                for (i = 0; i < b.length / 2; i++) {
                    b[(b.length / 2) + i] = element[(element.length - i) - 2];
                }
                return b;
            }
        });
        byte[] b2 = new byte[(bytes.size() * 8)];
        for (int i = 0; i < b2.length; i++) {
            b2[i] = ((byte[]) bytes.get(i % bytes.size()))[i / bytes.size()];
        }
        try {
            MessageDigest digest = MessageDigest.getInstance("MD5");
            digest.update(b2);
            byte[] messageDigest = digest.digest();
            StringBuilder hexString = new StringBuilder();
            for (byte aMessageDigest : messageDigest) {
                String h = Integer.toHexString(aMessageDigest & 255);
                while (h.length() < 2) {
                    h = "0" + h;
                }
                hexString.append(h);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            return "";
        }
    }
}