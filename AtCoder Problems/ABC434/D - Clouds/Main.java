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


public class Main{
  public static void main(String[] args){
    FastScanner fs = new FastScanner();
    PrintWriter out = new PrintWriter(System.out);

    long[][] a = new long[2025][2025];
    long[][] b = new long[2025][2025];
    
    long N = fs.nextLong();

    for(long k = 1; k <= N; k++){
      long U = fs.nextLong();
      long D = fs.nextLong();
      long L = fs.nextLong();
      long R = fs.nextLong();
      D += 1;
      R += 1;

      a[(int)U][(int)L] += 1;
      a[(int)U][(int)R] -= 1;
      a[(int)D][(int)L] -= 1;
      a[(int)D][(int)R] += 1;
      b[(int)U][(int)L] += k;
      b[(int)U][(int)R] -= k;
      b[(int)D][(int)L] -= k;
      b[(int)D][(int)R] += k;
    }

    for(long i = 0; i < 2025; i++){
      for (long j = 0; j < 2025; j++){
        if (j != 0){
          a[(int)i][(int)j] += a[(int)i][(int)(j-1)];
          b[(int)i][(int)j] += b[(int)i][(int)(j-1)];
        }
      }
    }

    for (long i = 0; i < 2025; i++){
      for (long j = 0; j < 2025; j++){
        if (i != 0){
          a[(int)i][(int)j] += a[(int)(i-1)][(int)j];
          b[(int)i][(int)j] += b[(int)(i-1)][(int)j];
        }
      }
    }
    
    long[] bk = new long[(int)N + 1];
    for (int i = 1; i <= 2000; i++) {
      for (int j = 1; j <= 2000; j++) {
        if (a[i][j] == 0) {
          bk[0]++;
        } else if (a[i][j] == 1) {
          if (b[i][j] >= 0 && b[i][j] <= N) {
            bk[(int)b[i][j]]++;
          }
        }
      }
    }
    for (int i = 1; i <= N; i++) {
      out.println(bk[0] + bk[i]);
    }
    out.flush();
  }
}