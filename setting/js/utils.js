class Utils {
  title(p) {
    if (p.alias) {
      var alias = p.alias.startsWith("@") ? p.file.name : p.alias;
      if (p.title.indexOf(alias) >= 0) {
        let t = `[[` + p.file.name + `|` + alias + `]]`;
        return p.title.replace(alias, t);
      } else {
        return `[[` + p.file.name + `|` + alias + `]] *|* ` + p.title;
      }
    } else {
      return `[[` + p.file.name + `|` + p.title + `]]`;
    }
  }
}
