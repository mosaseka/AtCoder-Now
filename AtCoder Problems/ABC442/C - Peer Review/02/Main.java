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

    int N = fs.nextInt();
    int M = fs.nextInt();

    int[][] AB_LIST = new int[M][2];
    for (int i = 0; i < M; i++) {
      AB_LIST[i][0] = fs.nextInt();
      AB_LIST[i][1] = fs.nextInt();
    }

    Set<Integer>[] CONFLICT = new HashSet[N + 1];
    for (int i = 0; i <= N; i++) {
      CONFLICT[i] = new HashSet<Integer>();
    }

    for (int i = 0; i < M; i++) {
      int a = AB_LIST[i][0];
      int b = AB_LIST[i][1];
      CONFLICT[a].add(b);
      CONFLICT[b].add(a);
    }

    List<Integer> ANSWER = new ArrayList<>();
    for (int i = 1; i <= N; i++) {
      int CHECK = N - 1 - CONFLICT[i].size();
      if (CHECK < 3) {
        ANSWER.add(0);
      } else {
        ANSWER.add(CHECK * (CHECK - 1) * (CHECK - 2) / 6);
      }
    }

    for (int i = 0; i < ANSWER.size(); i++) {
      if (i > 0) out.println(" ");
      out.println(ANSWER.get(i));
    }
    out.flush();
  }
}