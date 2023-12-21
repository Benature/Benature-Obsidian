class ThisWeek {
  display(dv, text = "") {
    dv.span(`${text}`);

    const local = dv.date("now");
    const year = local.year;
    let weekNumber = local.weekNumber + 1;
    if (weekNumber > 52) {
      weekNumber -= 52;
    }
    if (weekNumber < 10) {
      weekNumber = `0${weekNumber}`;
    }

    function filter(tasks) {
      for (var t of tasks) {
        filter(t.subtasks);
        t.subtasks = t.subtasks.filter((s) => !s.completed);
        // t.subtasks = t.subtasks.filter((s) => !s.fullyCompleted);
      }
    }
    var weekPages = dv.pages(`"Diary/Weekly/${year}-${weekNumber}W"`);
    if (weekPages.length == 0) {
      weekPages = dv.pages(`"Diary/Weekly/${year}-${weekNumber - 1}W"`);
      if (weekPages.length == 0) {
        return;
      }
    }
    var weekPage = weekPages.first();

    var tasks = weekPage.file.tasks.where((t) => !t.fullyCompleted);
    filter(tasks);

    // for (let group of tasks.groupBy((t) => t.header)) {
    //   dv.header(6, group.key);
    //   dv.taskList(group.rows);
    // }
    dv.span(` / ${weekPage.file.link}`);
    dv.el("ignore-next-dv", ""); // with css, set the header display to be none
    dv.taskList(tasks);
    // dv.paragraph(`$\\qquad$from ` + weekPage.file.link);

    // dv.span(weekPage);
    // dv.span(dv.current().file.ext == "md");
    // dv.paragraph(
    //   `日记 count: ` +
    //     dv.pages(`"Diary"`).filter((p) => p.file.ext == "md").length +
    //     `\n` +
    //     `笔记 count: ` +
    //     dv.pages(`-"Diary"`).filter((p) => p.file.ext == "md").length
    // );
  }
}
