package pbi.executor;

import android.os.Environment;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.zip.InflaterInputStream;
import pbi.executor.PyThread;
import pbi.executor.exceptions.*;
import pbi.executor.io.BytesIO;
import pbi.executor.types.*;
import pbi.executor.unicode.AggregateTranslator;
import pbi.executor.unicode.CharSequenceTranslator;
import pbi.executor.unicode.LookupTranslator;
import pbi.executor.unicode.UnicodeEscapeIgnorer;
import pbi.executor.unicode.UnicodeEscaper;
import pbi.executor.xml.OCL;
import pbi.executor.xml.PySQLite;
import pbi.executor.xml.ResourceManager;
import pbi.sc2.Meaterson;

public class Main {
  public static final CharSequenceTranslator ESCAPE_JAVA;
  public static final CharSequenceTranslator ESCAPE_JAVA2;
  public static final Map<CharSequence, CharSequence> JAVA_CTRL_CHARS_ESCAPE;
  static {
    final Map<CharSequence, CharSequence> initialMap = new HashMap<>();
    initialMap.put("\b", "\\b");
    initialMap.put("\n", "\\n");
    initialMap.put("\t", "\\t");
    initialMap.put("\f", "\\f");
    initialMap.put("\r", "\\r");
    initialMap.put("ё", "ё");
    initialMap.put("Ё", "Ё");
    JAVA_CTRL_CHARS_ESCAPE = Collections.unmodifiableMap(initialMap);
    
    final Map<CharSequence, CharSequence> escapeJavaMap = new HashMap<>();
    escapeJavaMap.put("'", "\\'");
    escapeJavaMap.put("\\", "\\\\");
    ESCAPE_JAVA = new AggregateTranslator(
      new LookupTranslator(Collections.unmodifiableMap(escapeJavaMap)),
      new LookupTranslator(JAVA_CTRL_CHARS_ESCAPE),
      new UnicodeEscapeIgnorer('а', 'я'),
      new UnicodeEscapeIgnorer('А', 'Я'),
      UnicodeEscaper.outsideOf(32, 0x7f)
    );
    
    final Map<CharSequence, CharSequence> escapeJavaMap2 = new HashMap<>();
    escapeJavaMap2.put("\"", "\\\"");
    escapeJavaMap2.put("\\", "\\\\");
    ESCAPE_JAVA2 = new AggregateTranslator(
      new LookupTranslator(Collections.unmodifiableMap(escapeJavaMap2)),
      new LookupTranslator(JAVA_CTRL_CHARS_ESCAPE),
      new UnicodeEscapeIgnorer('а', 'я'),
      new UnicodeEscapeIgnorer('А', 'Я'),
      UnicodeEscaper.outsideOf(32, 0x7f)
    );
    /*String str = "lol";
    for (int i = 0; i < 10; i++) {
      System.out.println(str);
      str = escapePython(str);
    }*/
  }
  public static final String escapeJava(final String input) {
    return ESCAPE_JAVA.translate(input);
  }
  public static final String escapePython(final String input) {
    if (input.indexOf("'") == -1)
      return "'" + ESCAPE_JAVA.translate(input) + "'";
    if (input.indexOf('"') == -1)
      return '"' + ESCAPE_JAVA2.translate(input) + '"';
    return "'" + ESCAPE_JAVA.translate(input) + "'";
  }

  private static void _print(Object obj) {
    Meaterson.print(obj);
  }
  private static void _print2(Object obj) {
    Meaterson.print2(obj);
  }

  public static void print(Object str) {
    Object obj = str instanceof Double ? new pFloat((double) str).__str__() : str;
    _print2(obj);
  }
  public static void print2(Object str) {
    Object obj = str instanceof Double ? new pFloat((double) str).__str__() : str;
    _print(obj);
  }

  static StringBuilder obj2sb(Object... str) {
    StringBuilder sb = new StringBuilder();
    int pos = 1, len = str.length;
    if (len > 0) sb.append(str[0]);
    while (pos < len) {
      sb.append(" ");
      Object s = str[pos];
      sb.append(s instanceof Double ? new pFloat((double) s).__str__() : s);
      pos++;
    }
    return sb;
  }
  public static void print(Object... str) {
    _print2(obj2sb(str));
  }
  public static void print2(Object... str) {
    _print(obj2sb(str));
  }

  static String toHex(byte[] arr) {
    StringBuffer sb = new StringBuffer();
    for (byte b : arr) sb.append(String.format("%02x", b));
    return sb.toString();
  }
  static String toHexBin(byte[] arr) {
    StringBuffer sb = new StringBuffer();
    for (byte b : arr) sb.append(b == 0 ? "0" : "1");
    return sb.toString();
  }
  public static void printObj(StringBuilder sb, Object obj, int level) {
    if (obj instanceof Object[]) {
      Object arr[] = (Object[]) obj;
      sb.append("{");
      int pos = 1, len = arr.length;
      level++;
      if (len > 0) printObj(sb, arr[0], level);
      while (pos < len) {
        sb.append(", ");
        printObj(sb, arr[pos], level);
        pos++;
      }
      sb.append("}");
    } else if (obj instanceof byte[])
      sb.append(toHex((byte[]) obj));
    else if (obj instanceof java.util.List<?>) {
      java.util.List<?> list = (java.util.List<?>) obj;
      sb.append("List(");
      boolean first = true;
      for (Object obj2 : list) {
        if (first) first = false;
        else sb.append(", ");
        printObj(sb, obj2, level + 1);
      }
      sb.append(")");
    } else if (obj instanceof int[]) {
      sb.append("int[]{");
      int arr[] = (int[]) obj;
      for (int i = 0; i < arr.length; i++) {
        if (i != 0) sb.append(", ");
        sb.append(arr[i]);
      }
      sb.append("}");
    } else if (obj instanceof String) {
      String str = (String) obj;
      sb.append("'" + str + "'");
    } else if (obj == null)
      sb.append("null");
    else if (obj instanceof Integer) {
      int num = (int) obj;
      sb.append(num);
    //} else if (obj instanceof CVoid)
    //  sb.append("Void");
    } else if (obj instanceof Bytes) {
      byte[] data = ((Bytes) obj).data;
      int L = data.length;
      if (L > 64) {
        sb.append(new Bytes(Arrays.copyOfRange(data, 0, 32)).__repr__());
        sb.append("...");
        sb.append(new Bytes(Arrays.copyOfRange(data, L - 32, L)).__repr__());
      } else sb.append(new Bytes(data).__repr__());
    } else if (obj instanceof Base)
      sb.append(((Base) obj).__repr__());
    else if (obj instanceof Map) {
      sb.append("Map{");
      boolean next = false;
      for (Map.Entry<?,?> entry : ((Map<?,?>) obj).entrySet()) {
        if (next) sb.append(", ");
        printObj(sb, entry.getKey(), level + 1);
        sb.append(": ");
        printObj(sb, entry.getValue(), level + 1);
        next = true;
      }
      sb.append("}");
    } else if (obj instanceof Class)
      sb.append((Class<?>) obj);
    else if (obj instanceof Boolean)
      sb.append((boolean) obj);
    else sb.append("???{|" + obj + "|" + obj.getClass() + "|}");
  }
  public static void printObj(StringBuilder sb, String str, Object obj) {
    sb.append(str);
    printObj(sb, obj, 0);
    sb.append("\n");
  }
  public static void printObj(StringBuilder sb, Object... objs) {
    for (Object obj: objs)
      if (obj instanceof String) sb.append((String) obj);
      else printObj(sb, obj, 0);
  }
  public static void printObj(Object... objs) {
    StringBuilder sb = new StringBuilder();
    printObj(sb, objs);
    _print(sb);
  }
  static void heap(int n, byte[] arr, byte[] res, int[] pos) {
    if (n >= arr.length) return;
    res[n] = arr[pos[0]++];
    heap(n * 2 + 1, arr, res, pos);
    heap(n * 2 + 2, arr, res, pos);
  }
  static int r_int(ByteBuffer bf) {
    byte b = bf.get();
    if ((b & 128) == 128) return b & 127 | r_int(bf) << 7;
    return b;
  }
  static int r_sint(ByteBuffer bf) {
    int num = r_int(bf);
    if ((num & 1) == 1) return -(num + 1) / 2;
    return num / 2;
  }
  static pFloat r_float(ByteBuffer bf) {
    return new pFloat(bf.getDouble());
  }
  static Base r_bigint(ByteBuffer bf) {
    int L = r_int(bf);
    if (L == 0) return r_float(bf);
    boolean pos = (L & 1) == 1;
    L >>= 1;
    byte[] buff = new byte[L + 1];
    bf.get(buff, 1, L);
    BigInt num = new BigInt(buff);
    if (pos) return num;
    return num.__neg__();
  }
  static byte[] r_str(int L, ByteBuffer bf, int limit) {
    int pos = 0;
    byte[] res = new byte[L];
    if (limit < 0 || L < limit) {
      byte[] bits = new byte[L * 8];
      for (int i = 0; i < L; i++) {
        byte b = bf.get();
        for (int j = 7; j >= 0; j--) bits[pos++] = (byte)(b >> j & 1);
      }
      pos = 0;
      for (int i = 0; i < L; i++) {
        byte b = 0;
        for (int j = 7; j >= 0; j--)
          b |= bits[pos / L + (pos++) % L * 8] << j;
        res[i] = b;
      }
    } else bf.get(res);
    return res;
  }
  static Base r_str(ByteBuffer bf) {
    int L = r_int(bf);
    Bytes b = new Bytes(r_str(L >> 1, bf, 123456));
    boolean is_int = (L & 1) == 0;
    if (is_int) return b.__tostr();
    return b;
    //System.out.println("• '" + str + "'");
    //return str;
  }
  static int r_none(ByteBuffer bf) {
    return r_int(bf) - 1;
  }
  /* static String r_star(ByteBuffer bf) {
    int b = r_int(bf);
    switch (b) {
      case 0: return null;
      case 1: return "*";
      case 2: return "**";
      default: return String.valueOf(b - 3);
    }
  }*/
  static int r_var(ByteBuffer bf) {
    int num = r_int(bf);
    if ((num & 7) > 3) return num | r_int(bf) << 16;
    return num;
    /*int n = num >> 3;
    switch (num & 7) {
      case 0: return n;
      case 1: return "l" + n;
      case 2: return "g" + n;
      case 3: return "b" + n;
      default: return "n" + n + "_" + r_int(bf);
    }*/
  }
  static Object unpack(ByteBuffer bf, String struct, Base[] news) {
    int L = struct.length();

    boolean ok = true;
    char[] chars = struct.toCharArray();
    for (char let : chars)
      if (let != 'r' && let != 'i' && let != 'v' && let != 'd') { ok = false; break; }
    if (ok) {
      int[] res = new int[L];
      for (int i = 0; i < L; i++)
        switch (chars[i]) {
          case 'r': res[i] = r_int(bf); break;
          case 'i': res[i] = r_sint(bf); break;
          case 'v': res[i] = r_var(bf); break;
          case 'd': res[i] = r_int(bf); break;
        }
      return res;
    }

    Object[] res = new Object[L];
    //System.out.println("  pack:" + struct);
    for (int i = 0; i < L; i++) {
      Object d;
      switch (struct.charAt(i)) {
        case 'r': d = r_int(bf); break; // reg
        case 'i': d = r_sint(bf); break; // int
        case 'f': d = r_bigint(bf); break; // int
        case 'v': d = r_var(bf); break;  // var
        case 's': d = r_news(news, bf); break;  // news str
        case 'a': {
          int l = r_int(bf);
          int[] arr = new int[l];
          for (int j = 0; j < l; j++)
            arr[j] = r_int(bf);
          d = arr;
          break; }
        case 'b': {
          int l = r_int(bf);
          Object[] arr = new Object[l];
          for (int j = 0; j < l; j++)
            arr[j] = new Object[] { r_int(bf), bf.get() > 0 };
          d = arr;
          break; }
        case 'c': {
          int l = r_int(bf);
          int[] arr = new int[l];
          for (int j = 0; j < l; j++) arr[j] = r_var(bf);
          d = arr;
          break; }
        case 'd': d = r_int(bf); break; // const
        case 'e': {
          int l = r_int(bf);
          int[][] arr = new int[l][];
          for (int j = 0; j < l; j++)
            arr[j] = new int[] { r_int(bf), r_int(bf) };
          d = arr;
          break; }
        default: d = null;
      }
      res[i] = d;
    }
    return res;
  }
  static Base r_const(ByteBuffer bf) {
    byte t = bf.get();
    switch (t) {
      case 0: return r_bigint(bf);
      case 1: return r_str(bf);
      case 2: return None;
      case 3: return False;
      case 4: return True;
      case 5:
        int L = r_int(bf);
        int[] arr = new int[L];
        for (int i = 0; i < L; i++) arr[i] = r_int(bf);

        return new TupleConst(arr);
      default: return None;
    }
  }
  static Base r_news(Base[] news, ByteBuffer bf) {
    int n = r_int(bf);
    try { return news[n]; }
    catch (ArrayIndexOutOfBoundsException e) {}
    String c = new StringBuilder().appendCodePoint(n).toString();
    return new pString(c);
  }
  void executor(String data) {
    double start = Functions.time();
    int L = data.length();
    int heap_len = L >> 1;
    byte[] arr = new byte[heap_len];
    for (int i = 0; i < data.length(); i += 2) {
      String b = data.substring(i, i + 2);
      arr[i >> 1] = (byte) Integer.parseInt(b, 16);
    }
    double end = Functions.time();
    Main.print("executor (2):", end - start);
    executor(arr);
  }
  void executor(byte[] arr) {
    double T1 = Functions.time();

    int heap_len = arr.length;
    byte[] arr2 = new byte[heap_len];
    int[] pos = {0};
    heap(0, arr, arr2, pos);

    double T2 = Functions.time();
    Main.print("heap:", T2 - T1);

    ByteArrayInputStream bais = new ByteArrayInputStream(arr2);
    InflaterInputStream iis = new InflaterInputStream(bais);
    ByteArrayOutputStream buffer = new ByteArrayOutputStream();
    int nRead;
    byte[] buff = new byte[256];
    try {
      while ((nRead = iis.read(buff, 0, buff.length)) != -1)
        buffer.write(buff, 0, nRead);
    } catch (IOException e) { e.printStackTrace(); }
    byte[] unc = buffer.toByteArray();
    /*byte[] unc = new byte[300000];
    try {
      int nRead = iis.read(unc, 0, unc.length);
    } catch (IOException e) { e.printStackTrace(); }
    */

    ByteBuffer bf = ByteBuffer.wrap(unc);

    double T3 = Functions.time();
    Main.print("zlib:", T3 - T2);

    g_count = r_int(bf);
    b_count = r_int(bf);
    int defs_n = r_int(bf);
    int c_count = r_int(bf);
    int news_n = r_int(bf);
    builtins = new Base[b_count];
    for (int i = 0; i < b_count; i++) {
      int k = r_int(bf);
      int v = r_int(bf);
      if (builtins_arr.length <= k) System.out.println("Нет builtin'а на позиции " + k);
      builtins[v] = builtins_arr[k];
    }
    consts = new Base[c_count];
    for (int i = 0; i < c_count; i++) consts[i] = r_const(bf); 
    for (int i = 0; i < c_count; i++) {
      Base data = consts[i];
      if (data instanceof TupleConst) ((TupleConst) data).load(consts, i);
    }
    //printObj("consts: ", consts, "\n");

    int L = pool_arr.length, pos2 = L;
    Base[] news = new Base[L + news_n];
    for (int i = 0; i < L; i++) {
      String s = pool_arr[i];
      if (s.startsWith("$attr$")) s = s.substring(6);
      news[i] = new pString(s);
    }
    for (int i = 0; i < news_n; i++) news[pos2++] = r_str(bf);
    //printObj("news: ", news, " ", news.length, "\n");

    // System.out.println("g: " + g_count + " b: " + b_count + " defs: " + defs_n);
    defs = new Object[defs_n];

    String[] packs = (
      "rr|rrr|r|r|rri|rr|rrr|ri|rr|i|" + // 0 - 9
      "rd|rv|vr|r|rr|rr|rr|rr|rr|rr|" +  // 10 - 19
      "rr|rr|rr|rr|rr|rr|rr|rr|rr|rr|" + // 20 - 29
      "rr|rr|rr|rr|rr|r|rrr|ra|rrs|r|" + // 30 - 39
      "rrr|rsr|vr||d|rb|c|r|v|r|" +      // 40 - 49
      "r|r|r|r|rr|rd|rr|r|rr|vs|" +      // 50 - 59
      "rr|rr|rr|rr|rrr|rrri|vrr|vri|re|rr|" + // 60 - 69
      "rrr|rrr|rrr|rrr|rrr|rrr|rrr|rrr|rrr|rrr|" + // 70 - 79
      "rrr|rrr|rrr|rrr|rrr|rrr|rrr|rrr|rrr|rrr|" + // 80 - 89
      "rrr|rr|rra|rr|rr|rr|rr|rre" // 90 - 97
    ).split("\\|");

    for (int id = 0; id < defs_n; id++) {
      //System.out.print(id + " | " + bf.position());
      int l_count = r_int(bf);
      int l = r_int(bf);
      int r_count = r_int(bf);

      String names[] = new String[l];
      try {
        for (int j = 0; j < l; j++)
          names[j] = r_news(news, bf).__str().str;
      } catch (TypeError e) { e.printStackTrace(); }

      l = r_int(bf);
      int[] loc_args_0 = new int[l];
      int[] loc_args_1 = new int[l];
      int without_default = 0, value;
      for (int j = 0; j < l; j++) {
        loc_args_0[j] = r_int(bf);
        loc_args_1[j] = value = r_none(bf);
        if (value == -1) without_default++;
      }
      int star = r_none(bf);
      int dstar = r_none(bf);

      //System.out.println(" .. " + bf.position());
      l = r_int(bf);
      int[] codes = new int[l];
      Object[] code_data = new Object[l];
      for (int line = 0; line < l; line++) {
        int code = bf.get() & 255;
        //System.out.println("  " + code + " " + packs[code] + " | " + bf.position());
        codes[line] = code;
        code_data[line] = unpack(bf, packs[code], news);
      }

      Map<String, Integer> arg_links = new HashMap<>();
      l = r_int(bf);
      for (int j = 0; j < l; j++) {
        int key = r_int(bf);
        arg_links.put(String.valueOf(key), r_int(bf));
      }

      Object[] args = new Object[] {
        loc_args_0, loc_args_1,
        star, dstar,
        without_default, arg_links
      };

      l = r_int(bf);
      Object[] tries = new Object[l];
      for (int trie = 0; trie < l; trie++) {
        int a = r_int(bf);
        int b = r_int(bf);
        int ts_n = r_int(bf);
        int[][] ts = new int[ts_n][2];
        for (int j = 0; j < ts_n; j++) ts[j] = new int[] { r_var(bf), r_int(bf) };
        int to = r_int(bf) - 1;
        tries[trie] = new Object[] { a, b, ts, to };
      }

      defs[id] = new Object[] {
        l_count,   // 0   in RegLocs
        names,     // 1   here
        r_count,   // 2   in RegLocs
        args,      // 3   in RegLocs
        codes,     // 4   here
        code_data, // 5   here
        tries      // 6   here
      };
    }

    double T4 = Functions.time();
    Main.print("reader:", T4 - T3);

    // printObj("defs: ", defs);
    start_program();
  }

  int g_count, b_count;
  //public static Main self = new Main();
  Object[] defs;
  Base[] builtins, globals, consts;
  /*static Base[] builtins;
  public static Base[] globals;*/
  // Base res_value;

  public static NoneType None = new NoneType();
  public static pBoolean True = new pBoolean(true);
  public static pBoolean False = new pBoolean(false);
  public static NotImplementedType NotImpl = new NotImplementedType();
  public static EllipsisType Ellipsis = new EllipsisType();

  static Base FuT = Functions.type;
  static Base FuI = Functions.inst;
  static Base[] builtins_arr = {
    FuT.getattr("print", FuI),
    None,
    Range.type, // range
    FuT.getattr("time", FuI),
    FuT.getattr("wait", FuI),
    FuT.getattr("round", FuI),
    True,
    False,
    Enumerate.type, // enumerate
    Base._Ty_Pe_,   // object
    Type.type,      // type
    BigInt.type,    // int
    Slice.type,     // slice
    FuT.getattr("len", FuI),
    pString.type,   // str
    FuT.getattr("repr", FuI),
    List.type,      // list
    Tuple.type,     // tuple
    Dict.type,      // dict
    PyKeyError.type,   // KeyError
    PyIndexError.type, // IndexError
    PyValueError.type, // ValueError
    PyException.type,  // Exception
    PyTypeError.type,  // TypeError
    PyAttributeError.type, // AttributeError
    PyStopIteration.type,  // StopIteration
    pFloat.type,           // float
    FuT.getattr("open", FuI),
    PyOverflowError.type,  // OverflowError
    Bytes.type,    // bytes
    pBoolean.type, // bool
    FuT.getattr("dir", FuI),
    Complex.type,  // complex
    pSet.type,     // set
    FuT.getattr("min", FuI),
    FuT.getattr("max", FuI),
    FuT.getattr("sum", FuI),
    FuT.getattr("sorted", FuI),
    FuT.getattr("any", FuI),
    FuT.getattr("all", FuI),
    PyModuleNotFoundError.type, // ModuleNotFoundError
    FuT.getattr("getattr", FuI),
    FuT.getattr("setattr", FuI),
    FuT.getattr("def_pool", FuI),
    FuT.getattr("chr", FuI),
    FuT.getattr("ord", FuI),
    FuT.getattr("divmod", FuI),
    Json.type, // json
    FuT.getattr("pow", FuI),
    FuT.getattr("zip", FuI),
    FuT.getattr("map", FuI),
    FuT.getattr("bin", FuI),
    FuT.getattr("oct", FuI),
    FuT.getattr("hex", FuI),
    PyNameError.type,         // NameError
    PyZeroDivisionError.type, // ZeroDivisionError
    ResourceManager.type,
    PyThread.type,            // Thread
    BytesIO.type,
    FuT.getattr("exit", FuI),
    PySQLite.type,  // SQLite
    OCL.type,       // OnClickListener
    FuT.getattr("RunFloatingWindow", FuI),
    FuT.getattr("abs", FuI),
    FuT.getattr("print2", FuI),
    PyOSError.type, // OSError
    FuT.getattr("STORAGE", FuI),
    FuT.getattr("currentThread", FuI),
    FuT.getattr("runOnUiThread", FuI),
    FuT.getattr("runOnGLThread", FuI),
    FuT.getattr("await", FuI),
    FuT.getattr("treemap", FuI),
    FuT.getattr("treeset", FuI),
    FuT.getattr("hook", FuI),
    FuT.getattr("main_context", FuI),
    PyIOError.type,     // IOError
    PyLookupError.type, // LookupError
    PyIllegalAccessError.type,    // IllegalAccessError
    PyInstantiationError.type,    // InstantiationError
    PyInvocationTargetError.type, // InvocationTargetError
    PyNoSuchFieldError.type,      // NoSuchFieldError
    PyNoSuchMethodError.type,     // NoSuchMethodError
    PyNullPointerError.type,      // NullPointerError
    PyStructError.type,     // StructError
    PySystemExit.type,      // SystemExit
    PyUnpicklingError.type, // UnpicklingError
    PyPicklingError.type,   // PicklingError
    PyEOFError.type,        // EOFError
    PyRecursionError.type,  // RecursionError
    Ellipsis,
    PyAssertionError.type,   // AssertionError
  };
  static String[] pool_arr = MainPoolArr.pool_arr;





  Base get_var(RegLocs env, int n) throws NameError {
    Base obj;
    switch (n & 7) {
      case 0: obj = env.regs[n >> 3]; break;
      case 1: obj = env.locs[n >> 3]; break;
      case 2: obj = globals[n >> 3]; break;
      case 3: obj = builtins[n >> 3]; break;
      default: obj = env.scope.get((n & 0xffff) >> 3)[n >> 16];
    }
    if (obj == null) {
      final String[] names = new String[] {"regs", "locs", "globals", "builtins", "non_stack", "???", "???", "???"};
      throw new NameError("name '" + names[n & 7] + ":" + (n >> 3) + "' is not defined");
    }
    return obj;
  }
  Base get_reg(Base[] regs, int n) throws NameError {
    Base obj = regs[n];
    if (obj == null) throw new NameError("name 'regs:" + n + "' is not defined");
    return obj;
  }
  Base get_reg(Base[] regs, Object n) throws NameError {
    Base obj = regs[(int) n];
    if (obj == null) throw new NameError("name 'regs:" + n + "' is not defined");
    return obj;
  }
  Base get_const(Base[] regs, int num) throws NameError {
    if ((num & 1) == 0) {
      Base obj = regs[num >> 1];
      if (obj == null) throw new NameError("name 'regs:" + (num >> 1) + "' is not defined");
      return obj;
    }
    return consts[num >> 1];
  }
  void set_var(RegLocs env, int n, Base obj) {
    switch (n & 7) {
      case 0: env.regs[n >> 3] = obj; break;
      case 1: env.locs[n >> 3] = obj; break;
      case 2: globals[n >> 3] = obj; break;
      case 3: builtins[n >> 3] = obj; break;
      default: env.scope.get((n & 0xffff) >> 3)[n >> 16] = obj;
    }
  }





  int last_method = -1;
  PyException last_exc;

  Base method(RegLocs env) throws RuntimeError {
    int id = env.id;
    last_method = id;

    Object[] state = env.state;

    String[] names = (String[]) state[1];
    int[] codes = (int[]) state[4];
    Object[] code_data = (Object[]) state[5];
    Object[] tries = (Object[]) state[6];

    Base[] regs = env.regs;
    Base[] locs = env.locs;
    Map<Integer, Base[]> scope = env.scope;

    int pos = 0;

    int size, reg, len;
    Base obj;
    Tuple t;
    Object[] data;
    int[] idata;

    loop:
    while (true) {
      try {
        switch (codes[pos]) {
        case 0: // v%0 = [None] * %1
          idata = (int[]) code_data[pos];
          regs[idata[0]] = new List(idata[1]);
          break;
        case 1: // v%0[%1] = v%2
          idata = (int[]) code_data[pos];
          regs[idata[0]].__setitem__(idata[1], get_reg(regs, idata[2]));
          break;
        case 2: // v%0 = list()
          idata = (int[]) code_data[pos];
          regs[idata[0]] = new List();
          break;
        case 3: // v%0 = v%0.__iter__()
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__iter__();
          break;
        case 4: // try: v%0 = v%1.__next__()\nexcept StopIteration: goto %2
          idata = (int[]) code_data[pos];
          try {
            regs[idata[0]] = get_reg(regs, idata[1]).__next__();
          } catch (StopIteration e) {
            pos += idata[2];
            continue loop;
          }
          break;
        case 5: // test tuple & size %0: v%1
          idata = (int[]) code_data[pos];
          size = idata[0];
          obj = get_reg(regs, idata[1]);
          if (!(obj instanceof Tuple)) throw new TypeError("TODO: пока-что поддерживаются только tuple в распаковочных конструкциях");
          t = (Tuple) obj;
          len = t.arr.length;
          if (len > size) throw new ValueError("too many values to unpack (expected " + size + ")");
          if (len < size) throw new ValueError("not enough values to unpack (expected " + size + ", got " + len + ")");
          break;
        case 6: // v%0 = v%1[%2]
          idata = (int[]) code_data[pos];
          regs[idata[0]] = get_reg(regs, idata[1]).__getitem__(idata[2]);
          break;
        case 7: // ifn v%0: goto %1
          idata = (int[]) code_data[pos];
          if (!get_reg(regs, idata[0]).__bool()) {
            pos += idata[1];
            continue loop;
          }
          break;
        case 8: // v%0.append(v%1)
          idata = (int[]) code_data[pos];
          //get_reg(idata[0]).__getattr__("append").__call__(get_reg(idata[1]));
          get_reg(regs, idata[0]).append(get_reg(regs, idata[1]));
          break;
        case 9: // goto %0
          idata = (int[]) code_data[pos];
          pos += idata[0];
          continue loop;
        case 10: // константу в регистр
          idata = (int[]) code_data[pos];
          regs[idata[0]] = get_const(regs, idata[1]);
          break;
        case 11: // переменную в регистр
          idata = (int[]) code_data[pos];
          regs[idata[0]] = get_var(env, idata[1]);
          break;
        case 12: // регистр в переменную
          idata = (int[]) code_data[pos];
          set_var(env, idata[0], get_reg(regs, idata[1]));
          break;
        case 13: // v%0 = tuple(v%0) (tuplemaker)
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = new Tuple(regs[reg]);
          break;
        case 14: // +=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__add__(get_reg(regs, idata[1]));
          break;
        case 15: // -=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__sub__(get_reg(regs, idata[1]));
          break;
        case 16: // *=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__mul__(get_reg(regs, idata[1]));
          break;
        case 17: // @=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__matmul__(get_reg(regs, idata[1]));
          break;
        case 18: // /=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__truediv__(get_reg(regs, idata[1]));
          break;
        case 19: // %=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__mod__(get_reg(regs, idata[1]));
          break;
        case 20: // &=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__and__(get_reg(regs, idata[1]));
          break;
        case 21: // |=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__or__(get_reg(regs, idata[1]));
          break;
        case 22: // ^=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__xor__(get_reg(regs, idata[1]));
          break;
        case 23: // <<=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__lshift__(get_reg(regs, idata[1]));
          break;
        case 24: // >>=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__rshift__(get_reg(regs, idata[1]));
          break;
        case 25: // **=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__pow__(get_reg(regs, idata[1]));
          break;
        case 26: // //=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__floordiv__(get_reg(regs, idata[1]));
          break;
        case 27: // <
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__lt(get_reg(regs, idata[1]));
          break;
        case 28: // >
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__gt(get_reg(regs, idata[1]));
          break;
        case 29: // ==
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__eq(get_reg(regs, idata[1]));
          break;
        case 30: // >=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__ge(get_reg(regs, idata[1]));
          break;
        case 31: // <=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__le(get_reg(regs, idata[1]));
          break;
        case 32: // !=
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__ne(get_reg(regs, idata[1]));
          break;
        case 33: // in
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, idata[1]).__contains__(get_reg(regs, reg));
          break;
        case 34: // is
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg) == (Base) get_reg(regs, idata[1]) ? True : False;
          break;
        case 35: // v%0 = not v%0
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__bool() ? False : True;
          break;
        case 36: // v%0 = v%1[v%2]
          idata = (int[]) code_data[pos];
          regs[idata[0]] = get_reg(regs, idata[1]).__getitem__(get_reg(regs, idata[2]));
          break;
        case 37: { // v%0 = v%0(args)
          data = (Object[]) code_data[pos];
          int[] arr = (int[]) data[1];
          int arr_L = arr.length;
          Base[] arr2 = new Base[arr_L];
          for (int i = 0; i < arr_L; i++) arr2[i] = get_reg(regs, arr[i]);
          reg = (int) data[0];
          regs[reg] = get_reg(regs, reg).__call__(arr2, new HashMap<String, Base>());
          last_method = id;
          break; }
        case 38: // v%0 = v%1.%2
          data = (Object[]) code_data[pos];
          regs[(int) data[0]] = get_reg(regs, data[1]).__getattr__((Base) data[2]);
          break;
        case 39: // v%0 = [v%0]     makelist
          idata = (int[]) code_data[pos];
          reg = idata[0];
          ArrayList<Base> list = new ArrayList<>();
          list.add(get_reg(regs, reg));
          regs[reg] = new List(list);
          break;
        case 40: // v%0[v%1] = v%2
          idata = (int[]) code_data[pos];
          get_reg(regs, idata[0]).__setitem__(get_reg(regs, idata[1]), get_reg(regs, idata[2]));
          break;
        case 41: // v%0.%1 = v%2
          data = (Object[]) code_data[pos];
          get_reg(regs, data[0]).__setattr__((Base) data[1], get_reg(regs, data[2]));
          break;
        case 42: // %0 = def #%1     (function)
          idata = (int[]) code_data[pos];
          set_var(env, idata[0], new Wrapper(env, idata[1]));
          break;
        case 43: // return
          return None;
        case 44: // return c%0
          idata = (int[]) code_data[pos];
          return get_const(regs, idata[0]);
        case 45: { // v%0 = tuple(v%1_args)
          data = (Object[]) code_data[pos];
          Object[] arr = (Object[]) data[1];
          Base[] data1 = new Base[arr.length];
          int data_L = data1.length, sum = 0;
          for (int i = 0; i < data_L; i++) {
            Object[] pair = (Object[]) arr[i];
            Base item = get_reg(regs, pair[0]);
            if ((boolean) pair[1]) {
              Tuple tuple = item.__tuple2();
              sum += tuple.arr.length;
              data1[i] = tuple;
            } else {
              sum++;
              data1[i] = item;
            }
          }
          if (sum > data_L) {
            Base[] data2 = new Base[sum];
            int poz = 0;
            for (int i = 0; i < data_L; i++)
              if ((boolean) ((Object[]) arr[i])[1]) {
                Base[] tuple = ((Tuple) data1[i]).arr;
                int tuple_L = tuple.length;
                System.arraycopy(tuple, 0, data2, poz, tuple_L);
                poz += tuple_L;
              } else data2[poz++] = data1[i];
            data1 = data2;
          }
          regs[(int) data[0]] = new Tuple(data1);
          break; }
        case 46: { // return type(id, (%0_args), locals())
          data = (Object[]) code_data[pos];
          int[] vars = (int[]) data[0];
          Base[] args = new Base[vars.length];
          for (int i = 0; i < vars.length; i++) args[i] = get_var(env, vars[i]);
          Map<String, Base> attrs = new HashMap<>();
          int l_count = locs.length;
          for (int i = 0; i < l_count; i++) attrs.put(names[i], locs[i]);
          return new Type(args, attrs); }
        case 47: // v%0 = dict()
          idata = (int[]) code_data[pos];
          regs[idata[0]] = new Dict();
          break;
        case 48: // %0 = last_exception
          idata = (int[]) code_data[pos];
          set_var(env, idata[0], last_exc);
          break;
        case 49: // raise v%0
          idata = (int[]) code_data[pos];
          obj = get_reg(regs, idata[0]);
          obj.__raise__();
          break;
        case 50: // v%0 = set()
          idata = (int[]) code_data[pos];
          regs[idata[0]] = new pSet();
          break;
        case 51: // v%0 = +v%0
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__pos__();
          break;
        case 52: // v%0 = -v%0
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__neg__();
          break;
        case 53: // v%0 = ~v%0
          idata = (int[]) code_data[pos];
          reg = idata[0];
          regs[reg] = get_reg(regs, reg).__invert__();
          break;
        case 54: // v%0 = v%1.__enter__()
          idata = (int[]) code_data[pos];
          regs[idata[0]] = get_reg(regs, idata[1]).__enter__();
          break;
        case 55: { // if v%0.__exit__(c%1, c%1.args, None): raise c%s
          idata = (int[]) code_data[pos];
          Base err = get_const(regs, idata[1]);
          boolean is_err = err instanceof PyException;
          Base args2 = is_err ? ((PyException) err).args : None;
          boolean alarm = !get_reg(regs, idata[0]).__exit__(err, args2, None).__bool__().R;
          if (is_err && alarm) err.__raise__();
          break; }
        case 56: // v%0.add(v%1)
          idata = (int[]) code_data[pos];
          ((pSet) get_reg(regs, idata[0])).add(get_reg(regs, idata[1]));
          break;
        case 57: // v%0 = last_exc
          idata = (int[]) code_data[pos];
          regs[idata[0]] = last_exc;
          break;
        case 58: // if v%0: goto %1
          idata = (int[]) code_data[pos];
          if (get_reg(regs, idata[0]).__bool()) {
            pos += idata[1];
            continue loop;
          }
          break;
        case 59: // v%0 <- "package%1"
          data = (Object[]) code_data[pos];
          set_var(env, (int) data[0], new JavaWrap((pString) data[1]));
          break;
        case 60: // v%0 = reg v%1
          idata = (int[]) code_data[pos];
          regs[idata[0]] = obj = regs[idata[1]];
          if (obj == null) throw new NameError("name 'regs:" + idata[1] + "' is not defined");
          break;
        case 61: // v%0 = local %1
          idata = (int[]) code_data[pos];
          obj = locs[idata[1]];
          if (obj == null) throw new NameError("name 'locs:" + idata[1] + "' is not defined");
          regs[idata[0]] = obj;
          break;
        case 62: // v%0 = global %1
          idata = (int[]) code_data[pos];
          obj = globals[idata[1]];
          if (obj == null) throw new NameError("name 'globals:" + idata[1] + "' is not defined");
          regs[idata[0]] = obj;
          break;
        case 63: // v%0 = builtin %1
          idata = (int[]) code_data[pos];
          obj = builtins[idata[1]];
          if (obj == null) throw new NameError("name 'builtins:" + idata[1] + "' is not defined");
          regs[idata[0]] = obj;
          break;
        case 64: // v%0 = scope %1 %2
          idata = (int[]) code_data[pos];
          obj = scope.get(idata[1])[idata[2]];
          if (obj == null) throw new NameError("name 'scope:" + idata[1] + ":" + idata[2] + "' is not defined");
          regs[idata[0]] = obj;
          break;
        case 65: // try: v%0 (test tuple & size %1) = v%2.__next__()\nexcept StopIteration: goto %3
          idata = (int[]) code_data[pos];
          try {
            regs[idata[0]] = obj = get_reg(regs, idata[2]).__next__();
          } catch (StopIteration e) {
            pos += idata[3];
            continue loop;
          }
          size = idata[1];
          if (!(obj instanceof Tuple)) throw new TypeError("TODO: пока-что поддерживаются только tuple в распаковочных конструкциях");
          t = (Tuple) obj;
          len = t.arr.length;
          if (len > size) throw new ValueError("too many values to unpack (expected " + size + ")");
          if (len < size) throw new ValueError("not enough values to unpack (expected " + size + ", got " + len + ")");
          break;
        case 66: // %0 = v%1[%2]
          idata = (int[]) code_data[pos];
          set_var(env, idata[0], get_reg(regs, idata[1]).__getitem__(idata[2]));
          break;
        case 67: // try: %0 = v%1.__next__()\nexcept StopIteration: goto %2
          idata = (int[]) code_data[pos];
          try {
            set_var(env, idata[0], get_reg(regs, idata[1]).__next__());
          } catch (StopIteration e) {
            pos += idata[2];
            continue loop;
          }
          break;
        case 68: { // v%0 = v%0(args)   args with stars
          data = (Object[]) code_data[pos];
          // printObj("args68:", line);
          int[][] args = (int[][]) data[1];
          int arr_L = args.length;
          ArrayList<Base> args2 = new ArrayList<>();
          Map<String, Base> dict = new HashMap<>();
          for (int i = 0; i < arr_L; i++) {
            int[] row = args[i];
            int type = row[0];
            Base item = get_reg(regs, row[1]);
            switch (type) {
              case 0: args2.add(item); break;
              case 1: // *
                for (Base item2 : item) args2.add(item2);
                break;
              case 2: // **
                Map<Base, Base> dict2 = item.__dict().get_dict();
                for (Map.Entry<Base, Base> kv : dict2.entrySet()) {
                  Base key = kv.getKey();
                  if (!(key instanceof pString)) throw new TypeError("keywords must be strings");
                  dict.put(((pString) key).str, kv.getValue());
                }
                break;
              default: // anc
                dict.put(String.valueOf(type - 3), item);
                break;
            }
          }
          reg = (int) data[0];
          Base[] args3 = new Base[args2.size()];
          args2.toArray(args3);
          regs[reg] = get_reg(regs, reg).__call__(args3, dict);
          last_method = id;
          break; }
        case 69: // v%0 = v%1.__iter__()   (3)
          idata = (int[]) code_data[pos];
          regs[idata[0]] = get_reg(regs, idata[1]).__iter__();
          break;
        default:
          throw new TypeError("• code_" + codes[pos] + " не реализован!");
        }
        pos++;
      } catch (StackOverflowError e) {
        throw new RecursionError(e.getMessage());
      } catch (Throwable eee) {
        RuntimeError e;
        if (eee instanceof RuntimeError) e = (RuntimeError) eee;
        else {
          printObj("last: line (" + id + ":" + pos + "): ", codes[pos], " ", code_data[pos]);
          e = new RuntimeError(eee);
        }
        e.addStackRecord(id, pos);

        last_exc = e.err;

        for (Object trie : tries) {
          Object[] trie2 = (Object[]) trie;

          int a = (int) trie2[0], b = (int) trie2[1], to = (int) trie2[3];
          int[][] ts = (int[][]) trie2[2];
          if (pos < a || pos >= b) continue;

          for (int[] ts2 : ts) {
            Type exc = (Type) get_var(env, ts2[0]);
            Class<?> c_exc = exc.get_obj();
            if (c_exc.isInstance(last_exc)) {
              pos = ts2[1];
              continue loop;
            }
          }
          if (to != -1) {
            pos = to;
            continue loop;
          }
        }
        throw e;
      }
    }
  }
  
  void start_program() {
    double T1 = Functions.time();

    globals = new Base[g_count];
    //Arrays.fill(globals, Void);
    // for (int i = 0; i < g_count; i++) globals[i] = Void;
    // printObj("globals: ", globals);
    // printObj("builtins: ", builtins);
    // printObj("builtins_arr: ", builtins_arr);
    try {
      Wrapper module = new Wrapper(this, 0);
      module.__call__();
      double T2 = Functions.time();
      Main.print("runtime:", T2 - T1);
    } catch (RuntimeError e) {
      print_error("• Ошибка исполнителя", e, this);
    } catch (Throwable e) {
      print_error("• Неотслеженная", e, this);
    }
  }
  
  /*public static void main(String[] args) {
    //String data = "789c6400e69bc980d5fb59e965ddbc4cddcaa9025455afb6c07a5f4acb7b73c473536466f212eaabfa2fde9b43d3d695dcd820cb8194aa89ca087981546a91c1686394967c81cec0c9c8c96d8c660991a270e0d78198ac870a34b68992119168246266ac9bb2529106262f49362e8d063e6033916161910671272b0046e76a26";
    //String data = "789c9241b3af4840081f203c87f4137f09b8037e460a595f7f25504461b422c71466a38b2336e2776b10d54387b25239daac6282b34d46f42576cde4b143f0d19400145bf01a884b08663ee151494b6b92fccb07ccf9ef802b14234ccb969a973475e790329646d3cae026ef924f234050838b7d71c29a80a66bbfc8c26a78d705bfc7c808efee1b21b2dd23f3a6040e7ad0fcd566768b5f7b10369e25d896fd3379121526e8f61a01bb3ed058bc4bae2e142404420632709adac24dbee8e4c96cdf24221ab22c4e72f5bc42405c4a75a63874ae08b39317bedbd7d05f9a721ebe9784220a39ce5878ac3aaefa6324ff19a81827d5ae200b8975ad5516848423ad2f8fbd8465b75855fb0dcd00a3ad9499684b28e0877542cc771faf9c25fa44538390f45dc73034268a8915a33178f1074d1a08eab377fc5735231cdd0b47b8aafdf32cb8a31bb03916502c21918158e484e87adca41af844c9f1043527158addcc2324c6140a0a41cc365912b43fc9bdeef5e50a48f3eca21f6db7b98d38d96f912ffd501876d8c9d17fc4d067921b279f3f293c9558206793";
    //String data = "789c5251f610589a44dadbb3f4855d0d4abbceb6cd08d224d03ccfe887fce60ae06de2f22d0a9a8bf807341ba0061e990dda3600fad5edf94bbc2d02b88ea2900814b1662403a9691a13218e8de9c471691017640435b8bc780c0df16ab40f9196734489af31a23f6da7e576b3fa8396e84288106f227b0a5142189aa91b001941029ad4a69701ab3683f4d43d4043ef061fe16e4b33399cd2047e23bb705c08514f5750df287d2940854e37c13a7dc8b1013b9e2282e7cdbaad7e093d9b81ba678cf79b360701ae4bc5a2e7631d057b0550c53782932425e777ef5e59c5beed76341f6084e3f2f4b097ca09f6a1d75b52bbd70f935cd856e6f2028ea0b8362ddd90c2d201d25c0ddc60cd97e254c99c1311e3c252b554cac4855764106fddd0cfa7c255765ff660beab3e08f46c6485da4d6bee35601f934b6d6e59a928d9b459eef29e23427899980645b8b245d26c624ef3664262149e6dc2499d51c22384fa3a43d0cfb4c823cc641edb5cb5e8c182c73943bf52e82ed5fa246179c717669fb86560a1bf035ebf1699337dbaf78de974b82133c0347d29f5fd91d8dfbd865765b6aa27269b3ba3566e543b487c36661567d18217a07df4b4a3d900319b3fec8ede7f4a4bfccf8df5553f04f64b945fb110201f739db3ab635b5065e7de074a5ea581ede674e55206155d58f6a589b56712ad5f83438e1a9a16a0bd3949d491a6d8d256ec8864ed61aaad7151642d289059f21a972ab88f31134a89bbbc3d885b957b1ed2f6ad03676742ec8aac87";
    //String data = "789c9241dd880bbe8e2df07ec687c475e67f5029c90be6b3e2416972b026912017d192ef1641dbd6d073cce85393c4d04535e8c441ec645d8adf778bae8e398edb8e29cb31ffb2b6f131f28c6b270a98f8c2342b000eaca7c0f33756abce5c2551c72846c15c720f36b8ecc70c1c4d827cfa5373995cd2b0b3002a1f71ce8e0317aa10bb08deabe736d49d67af73f36a035eca8f5e10bb6327302d26015556a1911c0ba604140262c15deca92087f3035e1c3f0b108aec5a7bf803681267567a4ff41f531f304fea6057706fc1827181a706947f30179aa126cbcd00ae4e861a0fbfc7911077381a5d901d7bf66e4afaa70a951b335078b7a423d6339c5527d2c4474bc1bb320589a053491b5389ec28ab27f25b432f1bb1f544a65eefff0f60dd678c4a04aa965c922a61af5d19012a88b58b22eb2e016a1986ce3d1540cbbc21f180d0948106ed1208bc64a164b2ba21062e30d9c700e6c74c15c34faf5b5f6d6b67721bd3c3593f0053714e3011f316ae9c11b9d2574853f102095c4ad1973420e6820f08d29aac4a36210643b6a4e2b3fa1534a62baaabc0812255467681f5f68527fb7160c481ad2fb1a8c8338402ab5897d1c390e5a009b0771eb0dfde897088717f8b947e61b17af9470bec5a779de2816e7f82381c548b4d5e2d7cf354e7d15839097bebd66932db667a7575942559048fa78fb155b9803587d1e8f4b518a724ea6fbb4a2ffeed21d5cea00b24b4bda519bccc9297628a79eed361f39b0cb160796818f357a8567dbd68c6ff1a1077e9d1b04aed931849d5ceaa76e2483b971906c5b26d37989ce78308f3946b1e7bbc7d42fdfcb2f16dd0b7c9eb";
    String data = Code.code;
    executor(data);
    if (self.limitter > 250) System.out.printf("limitter: Не выведено ещё %d строчек с тактами исполнителя\n", self.limitter - 100);
    System.out.println("Happy End!");
    System.out.println("📋📋📋📋📋📋📋📋📋📋");
    System.out.println(Functions.std_out.toString());
    System.out.println("📋📋📋📋📋📋📋📋📋📋");
  }*/
  
  
  
  // private static Wrapper[] def_pool = null;
  
  public static void runner() {
    ((Functions) FuI).defs.clear();
    /*new Thread(new Runnable() {
      public void run() {*/
        File f = new File("/sdcard/my_code3.asd");
        byte[] buff = null;
        try {
          FileInputStream fis = new FileInputStream(f);
          int L = fis.available();
          buff = new byte[L];
          fis.read(buff);
          fis.close();
        } catch (IOException e) {
          stackTrace(e);
          return;
        }
        Main yeah = new Main();
        yeah.readDebug("/sdcard/my_debug3.asd");
        try { yeah.executor(buff); }
        catch (Throwable e) { print_error("main_error", e, yeah); }
        // def_pool = get_defs();
    /*  }
    }).start();*/
  }
  
  /* public static Wrapper[] get_defs() {
    ArrayList<Wrapper> arr = new ArrayList<>();
    for (Base obj : globals)
      if (obj instanceof Wrapper) {
        Wrapper item = (Wrapper) obj;
        int id = item.id;
        while (arr.size() <= id) arr.add(null);
        arr.set(id, item);
      }
    arr.removeAll(Collections.singleton(null));
    Wrapper[] res = new Wrapper[arr.size()];
    arr.toArray(res);
    return res;
  }*/

  public static void print_error(String pref, Throwable e, Main yeah) {
    Throwable c = e.getCause();
    if (c instanceof RuntimeError) {
      ((RuntimeError) c).printStackTrace(pref, yeah.debug);
      return;
    }
    if (e instanceof RuntimeError) {
      ((RuntimeError) e).printStackTrace(pref, yeah.debug);
      return;
    }
    StringWriter sw = new StringWriter();
    e.printStackTrace(new PrintWriter(sw));
    String id = yeah == null ? "?" : Integer.toString(yeah.last_method);
    _print(pref + " (def #" + id + "): " + sw);
  }
  public static void print_error(String pref, Throwable e, Base caller) {
    Main yeah = caller.__main();
    print_error(pref, e, yeah);
  }

  public static void run_def(final int num, final Object... data) {
    new Thread(new Runnable() {
      public void run() {
        int L = data.length, i = 0;
        Base[] arr = new Base[L];
        for (Object obj : data) arr[i++] = JavaWrap.NewInstWrap(obj);
        // try { return def_pool[num].__call__(arr).__javadata(); }
        Base def = null;
        while (def == null) {
          try { def = ((Functions) FuI).defs.get(num); }
          catch (IndexOutOfBoundsException e) {}
          // if (def == null) { _print("DEF#" + num + " not found :/"); return null; }
        }
        try { /*return*/ def.__call__(arr).__javadata(); }
        catch (Throwable e) { print_error("error", e, def); }
      }
    }).start();
  }

  public static void stackTrace(Throwable e) {
    StringWriter sw = new StringWriter();
    e.printStackTrace(new PrintWriter(sw));
    print2(sw.toString());
  }
  public static void stackTrace() {
    try {
      int i = 0;
      i /= i;
    } catch (Throwable e) {
      stackTrace(e);
    }
  }

  Object debug = null;
  void readDebug(String path) {
    File f = new File(path);
    byte[] buff = new byte[0];
    try {
      FileInputStream fis = new FileInputStream(f);
      int L = fis.available();
      buff = new byte[L];
      fis.read(buff);
      fis.close();
    } catch (IOException e) { return; }

    ByteBuffer bf = ByteBuffer.wrap(buff);
    int codes_n = r_int(bf);
    String[][] codes = new String[codes_n][];
    for (int i = 0; i < codes_n; i++)
      codes[i] = new String[] {
        new String(r_str(r_int(bf), bf, -1), StandardCharsets.UTF_8),
        new String(r_str(r_int(bf), bf, -1), StandardCharsets.UTF_8)
      };

    HashMap<Integer, int[][]> map = new HashMap<>();
    int defs = r_int(bf);
    for (int i = 0; i < defs; i++) {
      int id = r_int(bf);
      int arrL = r_int(bf);
      int[][] arr = new int[arrL][];
      for (int j = 0; j < arrL; j++)
        arr[j] = new int[] { r_int(bf), r_int(bf), r_int(bf) };
      map.put(id, arr);
    }

    String[] attributes = new String(r_str(r_int(bf), bf, -1), StandardCharsets.UTF_8).split("\\|");
    String[] def_names = new String(r_str(r_int(bf), bf, -1), StandardCharsets.UTF_8).split("\\|");

    debug = new Object[] { codes, map, def_names };
    AttributeError.debug = attributes;
  }

  /*static {
    new JavaWrap(Base.class);
    
    int L = Type.ALL.size();
    String[] arr = new String[L];
    for (Map.Entry<?,?> entry : Type.ALL.entrySet())
      arr[(int) entry.getValue()] = (String) entry.getKey();
    print("Dict: " + Type.ALL);
    try {
      TextIOBase file = (TextIOBase) ((Functions) FuI).open("/sdcard/pool.txt", "w");
      
      file.write(new pString("attr_pool = (\n"));
      int i = 0;
      for (String item : arr)
        file.write(new pString("\"" + item + "\", # " + i++ + "\n"));
      file.write(new pString(")\n\n\n"));
      for (String item : arr)
        file.write(new pString("\"$attr$" + item + "\", "));
      file.write(new pString("\n"));
      file.close();
    } catch (Exception e) {}
  }*/

  public static void AddFD(String name, String data) {
    try {
      FileWriter fileWriter = new FileWriter(Environment.getExternalStorageDirectory() + File.separator + name, true);
      // FileWriter fileWriter = new FileWriter("/sdcard/" + name, true);
      fileWriter.write(data);
      fileWriter.write("\n");
      fileWriter.flush();
      fileWriter.close();
    } catch (Throwable e) {}
  }

  public static void Log(String data) {
    AddFD("MyEngine.log", data);
  }

  public static void reverse(byte[] arr) {
    if (arr == null) return;

    int j = arr.length - 1;
    for (int i = 0; j > i; i++) {
      byte tmp = arr[j];
      arr[j--] = arr[i];
      arr[i] = tmp;
    }
  }
}
