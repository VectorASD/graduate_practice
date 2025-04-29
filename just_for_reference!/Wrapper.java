package pbi.executor;

import java.util.HashMap;
import java.util.Map;
import pbi.executor.Main;
import pbi.executor.exceptions.RuntimeError;
import pbi.executor.types.*;

public class Wrapper extends Base {
  private static Map<String, Base> void_map = new HashMap<>();

  Main env;
  public int id;
  Map<Integer, Base[]> scope; // = new HashMap<Integer, Base[]>();
  Base[] prevRegs;

  public Wrapper(Main environment, int id, RegLocs env2) {
  //Map<Integer, RegLocs> s, Base[] prevRegs) {
    env = environment;
    this.id = id;
    scope = env2.scope;
    this.prevRegs = env2.regs;
  }
  @Override public Base __call__(Base[] args, Map<String, Base> dict) throws RuntimeError {
    return env.method(id, scope, prevRegs, args, dict);
  }
  @Override public Base __call__(Base... args) throws RuntimeError {
    return env.method(id, scope, prevRegs, args, void_map);
    //return __call__(args, new HashMap<String, Base>());
  }

  @Override public Main __main() { return env; }

  @Override public String __repr__() { return "<wrapper def#" + id + ">"; }
  static Type type = new Type(Wrapper.class, "wrapper");
  @Override public Type __type__() { return type; }
  @Override public pBoolean isdef() { return Main.True; }
}