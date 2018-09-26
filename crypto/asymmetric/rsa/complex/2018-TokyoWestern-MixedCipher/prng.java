public class Main {

   static int[] state;
   static int currentIndex;
40huo
   public static void main(String[] args) {
      state = new int[624];
      currentIndex = 0;

//    initialize(0);

//    for (int i = 0; i < 5; i++) {
//       System.out.println(state[i]);
//    }

      // for (int i = 0; i < 5; i++) {
      // System.out.println(nextNumber());
      // }

      if (args.length != 624) {
         System.err.println("must be 624 args");
         System.exit(1);
      }
      int[] arr = new int[624];
      for (int i = 0; i < args.length; i++) {
         arr[i] = Integer.parseInt(args[i]);
      }


      rev(arr);

      for (int i = 0; i < 6240huo4; i++) {
         System.out.println(state[i]);
      }

//    System.out.println("currentIndex " + currentIndex);
//    System.out.println("state[currentIndex] " + state[currentIndex]);
//    System.out.println("next " + nextNumber());

      // want -2065863258
   }

   static void nextState() {
      // Iterate through the state
      for (int i = 0; i < 624; i++) {
         // y is the first bit of the current number,
         // and the last 31 bits of the next number
         int y = (state[i] & 0x80000000)
               + (state[(i + 1) % 624] & 0x7fffffff);
         // first bitshift y by 1 to the right
         int next = y >>> 1;
         // xor it with the 397th next number
         next ^= state[(i + 397) % 624];
         // if y is odd, xor with magic number
         if ((y & 1L) == 1L) {
            next ^= 0x9908b0df;
         }
         // now we have the result
         state[i] = next;
      }
   }

   static int nextNumber() {
      currentIndex++;
      int tmp = state[currentIndex];
      tmp ^= (tmp >>> 11);
      tmp ^= (tmp << 7) & 0x9d2c5680;
      tmp ^= (tmp << 15) & 0xefc60000;
      tmp ^= (tmp >>> 18);
      return tmp;
   }

   static void initialize(int seed) {

      // http://code.activestate.com/recipes/578056-mersenne-twister/

      // global MT
      // global bitmask_1
      // MT[0] = seed
      // for i in xrange(1,624):
      // MT[i] = ((1812433253 * MT[i-1]) ^ ((MT[i-1] >> 30) + i)) & bitmask_1

      // copied Python 2.7's impl (probably uint problems)
      state[0] = seed;
      for (int i = 1; i < 624; i++) {
         state[i] = ((1812433253 * state[i - 1]) ^ ((state[i - 1] >> 30) + i)) & 0xffffffff;
      }
   }

   static int unBitshiftRightXor(int value, int shift) {
      // we part of the value we are up to (with a width of shift bits)
      int i = 0;
      // we accumulate the result here
      int result = 0;
      // iterate until we've done the full 32 bits
      while (i * shift < 32) {
         // create a mask for this part
         int partMask = (-1 << (32 - shift)) >>> (shift * i);
         // obtain the part
         int part = value & partMask;
         // unapply the xor from the next part of the integer
         value ^= part >>> shift;
         // add the part to the result
         result |= part;
         i++;
      }
      return result;
   }

   static int unBitshiftLeftXor(int value, int shift, int mask) {
      // we part of the value we are up to (with a width of shift bits)
      int i = 0;
      // we accumulate the result here
      int result = 0;
      // iterate until we've done the full 32 bits
      while (i * shift < 32) {
         // create a mask for this part
         int partMask = (-1 >>> (32 - shift)) << (shift * i);
         // obtain the part
         int part = value & partMask;
         // unapply the xor from the next part of the integer
         value ^= (part << shift) & mask;
         // add the part to the result
         result |= part;
         i++;
      }
      return result;
   }

   static void rev(int[] nums) {
      for (int i = 0; i < 624; i++) {

         int value = nums[i];
         value = unBitshiftRightXor(value, 18);
         value = unBitshiftLeftXor(value, 15, 0xefc60000);
         value = unBitshiftLeftXor(value, 7, 0x9d2c5680);
         value = unBitshiftRightXor(value, 11);

         state[i] = value;
      }
   }
}
