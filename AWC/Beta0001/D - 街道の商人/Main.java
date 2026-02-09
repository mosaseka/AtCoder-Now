import java.io.*;
import java.util.*;

public class Main{
  public static void main(String[] args){
    FastScanner fs = new FastScanner();
    PrintWriter out = new PrintWriter(System.out);

    final long NEG_INF = -(1L << 60);

    int N = fs.nextInt();
    int M = fs.nextInt();
    int K = fs.nextInt();

    long[] A = new long[N];
    int[] B = new int[N];
    for (int i = 0; i < N; i++) {
      A[i] = fs.nextLong();
      B[i] = fs.nextInt();
    }

    MonotonicDeque[] deque = new MonotonicDeque[M + 1];
    for (int i = 0; i <= M; i++){
      deque[i] = new MonotonicDeque();
    }

    long[] dp = new long[M + 1];
    long ans = 0;

    for (int i = 0; i < N; i++){
      int limit = i - K;
      limit = Math.max(limit, 0);
      
      for(int c = 0; c <= M; c++){
        deque[c].popExpired(limit);
        dp[c] = NEG_INF;
      }

      int bi = B[i];
      long ai = A[i];
      if (bi <= M){
        for (int c = bi; c <= M; c++){
          long prev = deque[c - bi].getMax();
          prev = Math.max(0, prev);
          dp[c] = prev + ai;
        }
      }

      for (int c = 0; c <= M; c++){
        if (dp[c] > ans){ans = dp[c];}
        if (dp[c] >= 0){deque[c].push(i, dp[c]);}
      }
    }
    out.println(ans);
    out.flush();
  }
}

class MonotonicDeque {
  private static class Pair {
    int idx;
    long val;
    Pair(int idx, long val) {
      this.idx = idx;
      this.val = val;
    }
  }
  
  private Deque<Pair> deque = new ArrayDeque<>();
  private final long NEG_INF = -(1L << 60);
  
  public void push(int idx, long val) {
    while (!deque.isEmpty() && deque.peekLast().val <= val) {
      deque.pollLast();
    }
    deque.addLast(new Pair(idx, val));
  }
  
  public void popExpired(int limit) {
    while (!deque.isEmpty() && deque.peekFirst().idx < limit) {
      deque.pollFirst();
    }
  }
  
  public long getMax() {
    if (deque.isEmpty()) return NEG_INF;
    return deque.peekFirst().val;
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