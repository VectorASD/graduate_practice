package pbi.executor;

import java.util.HashMap;
import java.util.Map;
import pbi.executor.types.Base;

public class RegLocs {
  public Base[] regs, locs;
  public Map<Integer, Base[]> scope;

  public RegLocs(int r_count, int ln_count, int id, Map<Integer, Base[]> scope) {
    regs = new Base[r_count];
    locs = new Base[ln_count];
    //Arrays.fill(regs, Main.Void);
    //Arrays.fill(locs, Main.Void);
    /* for (int i = 0; i < r_count; i++) regs[i] = Main.Void;
    for (int i = 0; i < ln_count; i++) locs[i] = Main.Void;*/
    scope = new HashMap<Integer, Base[]>(scope);
    scope.put(id, locs);
    this.scope = scope;
  }
}
