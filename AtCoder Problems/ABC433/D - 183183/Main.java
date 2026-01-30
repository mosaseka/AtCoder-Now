import java.io.*;
import java.util.*;

class FastScanner {
  private final InputStream in = System.in;
  private final byte[] buffer = new byte[1024];
  private int ptr = 0;
  private int buflen = 0;

  private boolean hasNextByte() {
    if (ptr < buflen) {
      return true;
    } else {
      ptr = 0;
      try {
        buflen = in.read(buffer);
      } catch (IOException e) {
        e.printStackTrace();
      }
      if (buflen <= 0) {
        return false;
      }
    }
    return true;
  }

  private int readByte() {
    if (hasNextByte())
      return buffer[ptr++];
    else
      return -1;
  }

  private static boolean isPrintableChar(int c) {
    return 33 <= c && c <= 126;
  }

  public boolean hasNext() {
    while (hasNextByte() && !isPrintableChar(buffer[ptr]))
      ptr++;
    return hasNextByte();
  }

  public String next() {
    if (!hasNext())
      throw new NoSuchElementException();
    StringBuilder sb = new StringBuilder();
    int b = readByte();
    while (isPrintableChar(b)) {
      sb.appendCodePoint(b);
      b = readByte();
    }
    return sb.toString();
  }

  public long nextLong() {
    if (!hasNext())
      throw new NoSuchElementException();
    long n = 0;
    boolean minus = false;
    int b = readByte();
    if (b == '-') {
      minus = true;
      b = readByte();
    }
    if (b < '0' || '9' < b) {
      throw new NumberFormatException();
    }
    while (true) {
      if ('0' <= b && b <= '9') {
        n *= 10;
        n += b - '0';
      } else if (b == -1 || !isPrintableChar(b)) {
        return minus ? -n : n;
      } else {
        throw new NumberFormatException();
      }
      b = readByte();
    }
  }

  public int nextInt() {
    long nl = nextLong();
    if (nl < Integer.MIN_VALUE || nl > Integer.MAX_VALUE)
      throw new NumberFormatException();
    return (int) nl;
  }

  public double nextDouble() {
    return Double.parseDouble(next());
  }
}

public class Main {
  public static void main(String[] args) {
    FastScanner fs = new FastScanner();
    PrintWriter out = new PrintWriter(System.out);

    long N = fs.nextLong();
    long M = fs.nextLong();
    long[] A = new long[(int)N];
    for (int i = 0; i < N; i++) {
      A[i] = fs.nextLong();
    }

    ArrayList<ArrayList<Integer>> g = new ArrayList<>();
    for (int i = 0; i < 11; i++) {
      g.add(new ArrayList<>());
    }

    for (long v : A) {
      g.get(String.valueOf(v).length()).add((int)(v % M));
    }

    for (ArrayList<Integer> gg : g) {
      Collections.sort(gg);
    }

    long ans = 0;

    for (long ai0 : A) {
      long ai = ai0;
      for (int k = 1; k <= 10; k++) {
        ai = (ai * 10) % M;
        long key = (M - ai) % M;
        ArrayList<Integer> list = g.get(k);
        int left = lowerBound(list, (int)key);
        int right = lowerBound(list, (int)(key + 1));
        ans += right - left;
      }
    }
    out.println(ans);
    out.flush();
  }

  static int lowerBound(ArrayList<Integer> list, int key) {
    int low = 0, high = list.size();
    while (low < high) {
      int mid = (low + high) / 2;
      if (list.get(mid) < key) {
        low = mid + 1;
      } else {
        high = mid;
      }
    }
    return low;
  }
}