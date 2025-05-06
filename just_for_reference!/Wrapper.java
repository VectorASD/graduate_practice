package pbi.executor;

import java.util.HashMap;
import java.util.Map;
import pbi.executor.Main;
import pbi.executor.exceptions.RuntimeError;
import pbi.executor.types.*;

public class Wrapper extends Base {
  private static Map<String, Base> void_map = new HashMap<>();
  private static Base[] void_regs = new Base[0];

  Main env;
  RegLocs reg_locs;

  public Wrapper(Main env, int id) {
    this.env = env;
    reg_locs = new RegLocs(env, id, void_regs, new HashMap<Integer, Base[]>());
  }

  public Wrapper(RegLocs prev, int id) {
    env = prev.env;
    reg_locs = new RegLocs(env, id, prev.regs, prev.scope);
  }

  @Override public Base __call__(Base[] a_args, Map<String, Base> kw_args) throws RuntimeError {
    reg_locs.argumentor(a_args, kw_args);
    return env.method(reg_locs);
  }
  @Override public Base __call__(Base... a_args) throws RuntimeError {
    reg_locs.argumentor(a_args, void_map);
    return env.method(reg_locs);
  }
  public Base call() throws RuntimeError {
    reg_locs.argumentor(void_regs, void_map);
    return env.method(reg_locs);
  }

  public int id() {
    return reg_locs.id;
  }
  public RegLocs reg_locs() {
    return reg_locs;
  }

  @Override public Main __main() { return env; }

  @Override public String __repr__() { return "<wrapper def#" + reg_locs.id + ">"; }
  static Type type = new Type(Wrapper.class, "wrapper");
  @Override public Type __type__() { return type; }
  @Override public pBoolean isdef() { return Main.True; }
}