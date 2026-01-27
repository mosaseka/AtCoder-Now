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

    int N = fs.nextInt();
    int K = fs.nextInt();
    long X = fs.nextLong();

    long[] A = new long[N];
    for (int i = 0; i < N; i++) A[i] = fs.nextLong();

    if (X <= 0) {
      out.println(1);
      out.flush();
      return;
    }

    Arrays.sort(A);

    long[] pref = new long[N + 1];
    for (int i = 0; i < N; i++) pref[i + 1] = pref[i] + A[i];

    for (int m = 1; m <= N; m++) {
      int t = m - (N - K);
      if (t <= 0) continue;

      int start = N - m;
      int end = start + t;
      long worst = pref[end] - pref[start];

      if (worst >= X) {
        out.println(m);
        out.flush();
        return;
      }
    }

    out.println(-1);
    out.flush();
  }
}