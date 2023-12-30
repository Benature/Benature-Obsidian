class Daily {
  setup(dv, R) {
    this.processTitle = function (p) {
      if (p.file.path.startsWith("Reading-notes")) {
        // return p.alias;
        // return p.file.link;
        return R.title(p) + ` (${p.year})`;
      } else {
        return p.file.link;
      }
    };

    this.processLink = function (links) {
      return links;
      if (links.length > 5) {
        return links.array().join(" | ");
      } else {
        return links;
      }
    };

    this.calDay = function (d, f = "YYYY/YYYY-MM-DD_ddd") {
      return window
        .moment(dv.current().file.day.plus({ days: d }).toString())
        .format(f);
    };
  }

  display(dv, luxon, R) {
    this.setup(dv, R);
    // this_.currentFilePath

    this.render_prev_next_daily_div(dv);

    this.render_yesterdayNotes(dv, luxon);
    this.render_todayDiaryInLastYears(dv);
    this.render_todayNotesInLastYears(dv);

    this.render_todayCreateAndModify(dv, luxon);
  }

  render_yesterdayNotes(dv, luxon) {
    // 昨日新建笔记
    const durNum = 1;
    const durType = "days";

    function timeSinceCreationInDays(p) {
      return luxon.Interval.fromDateTimes(
        p.file.ctime,
        dv.current().file.day
      ).length(durType);
    }

    var lastNotes = dv
      .pages(`-"Diary/Daily"`)
      .filter((p) => timeSinceCreationInDays(p) <= durNum);
    if (lastNotes.length) {
      // && lastNotes.length < 50
      dv.table(
        [`🧲 昨日新建`, "Inlinks"],
        lastNotes.map((p) => [
          this.processTitle(p),
          this.processLink(p.file.inlinks),
        ])
      );
    }
  }

  render_todayDiaryInLastYears(dv) {
    // 去年今日日记
    function findWeek(p) {
      let f = p.file;
      // return f;
      let weekFilePath = `"Diary/Weekly/${f.day.year}-${
        f.day.weekNumber + 1
      }W"`;
      // return weekFilePath;
      let week = dv.pages(weekFilePath);
      return week.file.link.first();
    }

    function titleInPast(p) {
      if (p.file.day.year > dv.current().file.day.year) {
        return `~~[[${p.file.name}]]~~`;
      } else {
        return p.file.link;
      }
    }
    var todayDiaryInLastYears = dv
      .pages(`"Diary/Daily" and #日记`)
      .where(
        (p) =>
          p.file.day.day === dv.current().file.day.day &&
          p.file.day.month === dv.current().file.day.month &&
          p.file.day.year != dv.current().file.day.year
      );
    if (todayDiaryInLastYears.length) {
      dv.table(
        [`💭 往年今日`, "OutLinks", "InLinks", "周课"],
        todayDiaryInLastYears
          .sort((p) => p.file.cday)
          .map((p) => [
            titleInPast(p),
            p.file.outlinks.where((l) => l.path.endsWith(".md")),
            p.file.inlinks,
            findWeek(p),
          ])
      );
    }
  }

  render_todayNotesInLastYears(dv) {
    // 去年今日笔记
    var todayNotesInLastYears = dv
      .pages(`-"Diary/Daily"`)
      .where(
        (p) =>
          p.file.cday.day === dv.current().day &&
          p.file.cday.month === dv.current().month
      );
    if (todayNotesInLastYears.length) {
      dv.table(
        [`📜 去年笔记`, "OutLinks"],
        todayNotesInLastYears
          .sort((p) => p.file.cday)
          .map((p) => [p.file.link, p.file.outlinks])
      );
    }
  }

  render_todayCreateAndModify(dv, luxon) {
    const TomorrowHour = 6;
    const current = dv.current().file;
    if (
      current.name ==
      window
        // .moment(luxon.DateTime.local().plus({ hour: -TomorrowHour }).toString())
        .moment(dv.date("now").plus({ hour: -TomorrowHour }).toString())
        .format("YYYY-MM-DD_ddd")
    ) {
      function selectToday(day) {
        return (
          day.day === current.day.day &&
          day.month === current.day.month &&
          day.year === current.day.year
        );
      }

      // 今日创建
      var todayCreateNotes = dv
        .pages(`-"Diary/Daily"`)
        .where((p) => selectToday(p.file.cday))
        .sort((p) => p.file.cday);

      //  今日修改
      var calDay = this.calDay;
      function filter(p) {
        return !(
          p.file.name == current.name ||
          p.file.name == calDay(-1, "YYYY-MM-DD_ddd") ||
          selectToday(p.file.cday)
        );
      }
      function setName(p) {
        if (p.file.path.startsWith("Reading-notes")) {
          if (p.alias) {
            return `[[${p.file.name}|${p.alias}]]`;
          }
          return `[[${p.file.name}]]`;
        }
        return p.file.link;
      }
      var todayModifyNotes = dv
        .pages(``)
        .where((p) => selectToday(p.file.mday))
        .where((p) => filter(p))
        .sort((p) => p.file.mtime, "desc");

      if (todayCreateNotes.length || todayModifyNotes.length) {
        dv.paragraph("");
        dv.el("center", "\\* \\* \\* 👇 𝓽𝓸𝓭𝓪𝔂 👇 * * *");
        dv.paragraph("");
        // 𝓪  𝓫  𝓬  𝓭  𝓮  𝓯  𝓰  𝓱  𝓲  𝓳  𝓴  𝓵  𝓶  𝓷  𝓸  𝓹  𝓺  𝓻  𝓼  𝓽  𝓾  𝓿  𝔀  𝔁  𝔂  𝔃
      }

      if (todayCreateNotes.length) {
        dv.table(
          [`🍀 今日新建 (` + todayCreateNotes.length + `)`, "Inlinks"],
          todayCreateNotes.map((p) => [
            this.processTitle(p),
            this.processLink(p.file.inlinks),
          ])
        );
      }

      if (todayModifyNotes.length) {
        let content = todayModifyNotes
          .map((p) => setName(p))
          .array()
          .join(" | ");
        dv.paragraph(`**今日修改 (${todayModifyNotes.length})：** ${content}`);
      }
    }
  }

  render_prev_next_daily_div(dv) {
    const weekDaySign = " ☽♂☿♃♀♄☼";
    const folder = `"Diary/Daily/`;
    const prevDay = dv.pages(folder + this.calDay(-1) + `.md"`).file;
    const nextDay = dv.pages(folder + this.calDay(+1) + `.md"`).file;

    const options = [
      {
        selector: "a.prev-daily",
        path: prevDay?.path[0],
        text: `< ${this.calDay(-1, "MM-DD ddd")} ${
          weekDaySign[dv.current().file.day.plus({ days: -1 }).weekday]
        }`,
      },
      {
        selector: "a.next-daily",
        path: nextDay?.path[0],
        text: `${
          weekDaySign[dv.current().file.day.plus({ days: 1 }).weekday]
        } ${this.calDay(1, "MM-DD ddd")} >`,
      },
    ];

    var content = ``;
    options.forEach(({ selector, path, text }) => {
      if (path != "") {
        content += `<a class="internal-link prev-daily elegant-btn ready" href="${path}">${text}</a>`;
      } else {
        content += `<a class="internal-link prev-daily elegant-btn"></a>`;
      }
    });
    dv.el("div", `<div class="breadcrumbs-wrapper"> ${content} </div>`);

    const last_week = dv.pages(folder + this.calDay(-7) + `.md"`).file;
    const last_month = dv.pages(folder + this.calDay(-30) + `.md"`).file;
    const last_season = dv.pages(folder + this.calDay(-90) + `.md"`).file;
    const last_half_year = dv.pages(folder + this.calDay(-180) + `.md"`).file;
    dv.el(
      "div",
      `<a class="internal-link" href="${
        last_week?.path[0]
      }">上周（${this.calDay(-7, "MM-DD")}）</a>` +
        `<a class="internal-link" href="${
          last_month?.path[0]
        }">上月（${this.calDay(-30, "MM-DD")}）</a>` +
        `<a class="internal-link" href="${
          last_season?.path[0]
        }">上季（${this.calDay(-90, "MM-DD")}）</a>` +
        `<a class="internal-link" href="${
          last_half_year?.path[0]
        }">上半年（${this.calDay(-180, "MM-DD")}）</a>`
    );
  }
}
