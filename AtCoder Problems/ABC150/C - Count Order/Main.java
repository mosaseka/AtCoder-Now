import java.io.*;
import java.util.*;

public class Main{
  public static void main(String[] args){
    FastScanner fs = new FastScanner();
    PrintWriter out = new PrintWriter(System.out);

    int N = fs.nextInt();

    int[] P = new int[N];
    for(int i = 0; i < N; i++){
      P[i] = fs.nextInt();
    }

    int[] Q = new int[N];
    for(int i = 0; i < N; i++){
      Q[i] = fs.nextInt();
    }

    long a = getIndex(P, N);
    long b = getIndex(Q, N);

    out.println(Math.abs(a - b));
    out.flush();
  }

  static long getIndex(int[] perm, int n){
    long[] fact = new long[n + 1];
    fact[0] = 1;
    for(int i = 1; i <= n; i++){
      fact[i] = fact[i - 1] * i;
    }

    boolean[] used = new boolean[n + 1];
    long index = 0;

    for(int i = 0; i < n; i++){
      int current = perm[i];
      int smallerCount = 0;
      for(int j = 1; j < current; j++){
        if(!used[j]){
          smallerCount++;
        }
      }
      index += smallerCount * fact[n - 1 - i];
      used[current] = true;
    }
    return index + 1;
  }
}


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