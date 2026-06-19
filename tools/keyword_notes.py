from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

# 配置数据（仅用于示例和展示）
DEMO_URL = "https://site-official-leyu.com.cn"
DEMO_KEYWORD = "乐鱼体育"


@dataclass
class NoteEntry:
    """单条关键词笔记条目"""
    keyword: str
    note: str
    tags: List[str] = field(default_factory=list)
    source_url: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def formatted(self) -> str:
        """返回格式化的单条笔记字符串"""
        parts = [
            f"关键词: {self.keyword}",
            f"笔记: {self.note}",
            f"标签: {', '.join(self.tags) if self.tags else '无'}",
            f"来源: {self.source_url or '未知'}",
            f"创建时间: {self.created_at}",
        ]
        return "\n".join(parts)


@dataclass
class KeywordNotesCollection:
    """关键词笔记集合"""
    title: str = "关键词笔记"
    notes: List[NoteEntry] = field(default_factory=list)

    def add_note(self, keyword: str, note: str, tags: Optional[List[str]] = None, source_url: Optional[str] = None) -> None:
        """添加一条新笔记"""
        entry = NoteEntry(
            keyword=keyword,
            note=note,
            tags=tags or [],
            source_url=source_url,
        )
        self.notes.append(entry)

    def find_by_keyword(self, keyword: str) -> List[NoteEntry]:
        """根据关键词查找笔记（精确匹配）"""
        return [n for n in self.notes if n.keyword == keyword]

    def find_by_tag(self, tag: str) -> List[NoteEntry]:
        """根据标签查找笔记"""
        return [n for n in self.notes if tag in n.tags]

    def remove_by_keyword(self, keyword: str) -> int:
        """删除所有匹配关键词的笔记，返回删除数量"""
        original_len = len(self.notes)
        self.notes = [n for n in self.notes if n.keyword != keyword]
        return original_len - len(self.notes)

    def summary(self) -> str:
        """返回整体概览文本"""
        lines = [
            f"标题: {self.title}",
            f"总笔记数: {len(self.notes)}",
            "---",
        ]
        for idx, entry in enumerate(self.notes, 1):
            lines.append(f"{idx}. {entry.keyword} — {entry.note[:30]}{'…' if len(entry.note) > 30 else ''}")
        return "\n".join(lines)


def format_notes_as_report(collection: KeywordNotesCollection, separator: str = "=" * 40) -> str:
    """将笔记集合格式化为完整报告"""
    report_parts = [
        separator,
        f"《{collection.title}》报告",
        f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        separator,
        f"关联示例 URL: {DEMO_URL}",
        f"关联示例关键词: {DEMO_KEYWORD}",
        separator,
    ]
    if not collection.notes:
        report_parts.append("（暂无笔记）")
    else:
        for i, entry in enumerate(collection.notes, 1):
            report_parts.append(f"笔记 #{i}")
            report_parts.append(entry.formatted())
            report_parts.append(separator)
    return "\n".join(report_parts)


def demo_run() -> None:
    """示例运行：展示基本用法"""
    collection = KeywordNotesCollection(title="我的关键词笔记")

    # 添加示例笔记
    collection.add_note(
        keyword=DEMO_KEYWORD,
        note="这是一条关于乐鱼体育平台的示例笔记，用于展示数据结构。",
        tags=["体育", "示例"],
        source_url=DEMO_URL,
    )
    collection.add_note(
        keyword="Python 学习",
        note="记录 Python 数据类（dataclass）的使用技巧。",
        tags=["编程", "Python"],
    )
    collection.add_note(
        keyword=DEMO_KEYWORD,
        note="第二条乐鱼体育相关笔记，用于测试关键词查找功能。",
        tags=["体育", "测试"],
        source_url=DEMO_URL,
    )

    # 查找演示
    print("查找关键词 '乐鱼体育' 的结果：")
    for note in collection.find_by_keyword(DEMO_KEYWORD):
        print(note.formatted())
        print("-" * 30)

    print("\n按标签 '体育' 查找：")
    for note in collection.find_by_tag("体育"):
        print(note.formatted())
        print("-" * 30)

    # 生成完整报告
    print("\n完整报告：")
    print(format_notes_as_report(collection))

    # 删除演示
    print(f"\n删除关键词 '{DEMO_KEYWORD}' 的笔记，共删除 {collection.remove_by_keyword(DEMO_KEYWORD)} 条。")
    print("删除后集合概览：")
    print(collection.summary())


if __name__ == "__main__":
    demo_run()