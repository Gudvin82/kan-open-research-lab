from dataclasses import dataclass


@dataclass(frozen=True)
class PageCopy:
    key: str
    title: str
    eyebrow: str
    summary: str
    description: str


@dataclass(frozen=True)
class ResearchCard:
    slug: str
    collection: str
    title: str
    summary: str
    method: str
    status: str
    evidence: str
    reproducibility: str
    boundary: str


@dataclass(frozen=True)
class Explanation:
    key: str
    label: str
    title: str
    body: str
    note: str


@dataclass(frozen=True)
class MethodCopy:
    slug: str
    title: str
    short_title: str
    summary: str
    purpose: str
    limitation: str
    explanations: tuple[Explanation, ...]


UI: dict[str, dict[str, str]] = {
    "ru": {
        "site_name": "KAN Open Research Lab",
        "site_short": "KAN / LAB",
        "skip": "Перейти к содержанию",
        "primary_nav": "Основная навигация",
        "home": "Главная",
        "research": "Исследования",
        "methods": "Методы",
        "knowledge": "База знаний",
        "about": "О проекте",
        "language": "Язык",
        "russian": "Русский",
        "english": "English",
        "github": "GitHub проекта",
        "mission": (
            "Открытая лаборатория о KAN, нейросетевых базовых линиях "
            "и проверяемых вычислительных исследованиях."
        ),
        "footer_research": "Исследования",
        "footer_knowledge": "Знания",
        "footer_project": "Проект",
        "scientific_disclaimer": (
            "Численный результат, низкая ошибка или найденная формула сами "
            "по себе не являются доказательством."
        ),
        "compute_label": "Вычислительный узел",
        "compute_status": "compute_node_unavailable",
        "compute_note": "Публичные материалы доступны независимо от worker.",
        "read_more": "Открыть раздел",
        "method_more": "Изучить метод",
        "explanation_nav": "Уровень объяснения",
        "what_supports": "Что поддерживает",
        "what_not": "Чего не доказывает",
        "status": "Статус",
        "method": "Метод",
        "evidence": "Доказательность",
        "reproducibility": "Воспроизводимость",
        "open_notice": "Задача остаётся открытой.",
        "known_label": "Воспроизводим известное",
        "open_label": "Исследуем открытое",
        "no_publications": "Материалы готовятся",
        "not_found_title": "Страница не найдена",
        "not_found_summary": (
            "Такого адреса нет. Проверьте ссылку или вернитесь на главную."
        ),
        "back_home": "Вернуться на главную",
    },
    "en": {
        "site_name": "KAN Open Research Lab",
        "site_short": "KAN / LAB",
        "skip": "Skip to content",
        "primary_nav": "Primary navigation",
        "home": "Home",
        "research": "Research",
        "methods": "Methods",
        "knowledge": "Knowledge Base",
        "about": "About",
        "language": "Language",
        "russian": "Русский",
        "english": "English",
        "github": "Project GitHub",
        "mission": (
            "An open laboratory for KAN, neural baselines and verifiable "
            "computational research."
        ),
        "footer_research": "Research",
        "footer_knowledge": "Knowledge",
        "footer_project": "Project",
        "scientific_disclaimer": (
            "A numerical result, low error or discovered formula is not, by "
            "itself, a proof."
        ),
        "compute_label": "Compute node",
        "compute_status": "compute_node_unavailable",
        "compute_note": "Public materials remain available without the worker.",
        "read_more": "Open section",
        "method_more": "Explore method",
        "explanation_nav": "Explanation level",
        "what_supports": "What it supports",
        "what_not": "What it does not prove",
        "status": "Status",
        "method": "Method",
        "evidence": "Evidence",
        "reproducibility": "Reproducibility",
        "open_notice": "The problem remains open.",
        "known_label": "Reproducing known results",
        "open_label": "Investigating open questions",
        "no_publications": "Materials in preparation",
        "not_found_title": "Page not found",
        "not_found_summary": (
            "This address does not exist. Check the link or return home."
        ),
        "back_home": "Return home",
    },
}


PAGES: dict[str, dict[str, PageCopy]] = {
    "ru": {
        "home": PageCopy(
            "home",
            "Исследования, которые можно проверить",
            "Открытая исследовательская лаборатория",
            (
                "Разбираем KAN, MLP и PINN без магии: воспроизводим известные "
                "результаты, честно описываем открытые вопросы и показываем "
                "границы каждого вывода."
            ),
            "Открытая лаборатория воспроизводимых исследований KAN, MLP и PINN.",
        ),
        "research": PageCopy(
            "research",
            "Исследования",
            "Статус важнее громкого результата",
            (
                "Два разных контура: независимое воспроизведение уже известных "
                "решений и проверяемый прогресс по вопросам, которые остаются "
                "открытыми."
            ),
            "Воспроизведения известных результатов и открытые задачи лаборатории.",
        ),
        "methods": PageCopy(
            "methods",
            "Методы без рейтинга любимчиков",
            "KAN рядом с базовыми линиями",
            (
                "KAN рассматривается вместе с MLP, PINN и корректными "
                "сравнительными экспериментами. Пока здесь — нейтральная "
                "карта методов, а не заявление о превосходстве."
            ),
            "Нейтральный обзор KAN, MLP, PINN и сравнительных экспериментов.",
        ),
        "knowledge": PageCopy(
            "knowledge",
            "База знаний",
            "От интуиции к формальному языку",
            (
                "Будущие разборы источников, терминов, формул и "
                "воспроизводимых примеров будут связаны с точными статусами "
                "и тремя уровнями объяснения."
            ),
            "База знаний лаборатории с проверяемыми источниками и объяснениями.",
        ),
        "about": PageCopy(
            "about",
            "О проекте",
            "Открытость — это метод работы",
            (
                "Код, спецификации и проверки живут в GitHub. Секреты, "
                "приватные данные и тяжёлые артефакты туда не попадают. "
                "Публикация отделена от эксперимента и требует проверки."
            ),
            "Миссия, правила научной честности и устройство проекта.",
        ),
    },
    "en": {
        "home": PageCopy(
            "home",
            "Research you can inspect",
            "Open research laboratory",
            (
                "We examine KAN, MLP and PINN without mystique: reproduce known "
                "results, state open questions honestly and show the boundary "
                "of every conclusion."
            ),
            "An open laboratory for reproducible KAN, MLP and PINN research.",
        ),
        "research": PageCopy(
            "research",
            "Research",
            "Status matters more than a loud result",
            (
                "Two distinct tracks: independent reproduction of established "
                "solutions and verifiable progress on questions that remain open."
            ),
            "Known-result reproductions and open research questions.",
        ),
        "methods": PageCopy(
            "methods",
            "Methods without favourites",
            "KAN alongside its baselines",
            (
                "KAN is considered together with MLP, PINN and fair comparison "
                "experiments. For now this is a neutral map, not a superiority "
                "claim."
            ),
            "A neutral introduction to KAN, MLP, PINN and comparisons.",
        ),
        "knowledge": PageCopy(
            "knowledge",
            "Knowledge Base",
            "From intuition to formal language",
            (
                "Future source notes, terms, equations and reproducible examples "
                "will carry exact statuses and three explanation levels."
            ),
            "Reviewed sources and layered explanations from the laboratory.",
        ),
        "about": PageCopy(
            "about",
            "About",
            "Openness is a working method",
            (
                "Code, specifications and checks live on GitHub. Secrets, "
                "private data and heavy artifacts do not. Publication is "
                "separate from experimentation and requires review."
            ),
            "Mission, scientific integrity rules and project architecture.",
        ),
    },
}


RESEARCH: dict[str, tuple[ResearchCard, ...]] = {
    "ru": (
        ResearchCard(
            "function-approximation-baseline",
            "reproduced",
            "Аппроксимация гладкой функции",
            "Учебный протокол для проверки реализации и честного сравнения.",
            "KAN · MLP",
            "Независимое воспроизведение",
            "Код и протокол планируются",
            "Пакет готовится",
            "Поддерживает проверку pipeline; не доказывает превосходство метода.",
        ),
        ResearchCard(
            "pinn-reference-case",
            "reproduced",
            "Эталонная краевая задача PINN",
            "Повторение опубликованной постановки с заранее заданными метриками.",
            "PINN · численный baseline",
            "Учебный материал",
            "Разбор источника",
            "Планируется",
            "Показывает постановку; не подтверждает новый научный результат.",
        ),
        ResearchCard(
            "kan-extrapolation",
            "open",
            "Устойчивость экстраполяции KAN",
            "Планируем серию сравнений по seed, сложности и области вне обучения.",
            "KAN · MLP",
            "Гипотеза",
            "Эксперимент ещё не опубликован",
            "Планируется",
            (
                "Задача остаётся открытой. Численный результат "
                "не является доказательством."
            ),
        ),
        ResearchCard(
            "interpretable-structure",
            "open",
            "Когда структура действительно интерпретируема?",
            "Отделяем красивую визуализацию от проверяемого структурного вывода.",
            "KAN · символический baseline",
            "Открытый вопрос",
            "Протокол формируется",
            "Планируется",
            "Задача остаётся открытой. Низкая ошибка не доказывает интерпретируемость.",
        ),
    ),
    "en": (
        ResearchCard(
            "function-approximation-baseline",
            "reproduced",
            "Smooth function approximation",
            "An educational protocol for implementation checks and fair comparison.",
            "KAN · MLP",
            "Independent reproduction",
            "Code and protocol planned",
            "Package in preparation",
            "Supports pipeline validation; does not prove method superiority.",
        ),
        ResearchCard(
            "pinn-reference-case",
            "reproduced",
            "Reference PINN boundary-value problem",
            "A published setup repeated with metrics fixed in advance.",
            "PINN · numerical baseline",
            "Educational material",
            "Source review",
            "Planned",
            "Explains the setup; does not establish a new scientific result.",
        ),
        ResearchCard(
            "kan-extrapolation",
            "open",
            "KAN extrapolation stability",
            "A planned comparison across seeds, complexity and out-of-domain ranges.",
            "KAN · MLP",
            "Hypothesis",
            "Experiment not yet published",
            "Planned",
            "The problem remains open. A numerical result is not a proof.",
        ),
        ResearchCard(
            "interpretable-structure",
            "open",
            "When is structure genuinely interpretable?",
            "Separating attractive visualisations from testable structural claims.",
            "KAN · symbolic baseline",
            "Open question",
            "Protocol in preparation",
            "Planned",
            "The problem remains open. Low error does not prove interpretability.",
        ),
    ),
}


def _explanations(locale: str, subject: str) -> tuple[Explanation, ...]:
    if locale == "ru":
        return (
            Explanation(
                "human",
                "По-человечески",
                "Зачем это нужно",
                (
                    f"{subject} — один из инструментов, а не готовый ответ. "
                    "Здесь мы объясняем идею без требований "
                    "к математической подготовке."
                ),
                "Интуитивная карта темы.",
            ),
            Explanation(
                "technical",
                "Технически",
                "Как устроен вычислительный подход",
                (
                    "Технический уровень фиксирует входы, архитектуру, метрики, "
                    "базовые линии и ограничения сравнения до просмотра результата."
                ),
                "Детали реализации появятся вместе с воспроизводимым протоколом.",
            ),
            Explanation(
                "scientific",
                "Научно",
                "Формальная граница утверждений",
                (
                    "Формальный уровень связывает определения и утверждения с "
                    "первоисточниками. Экспериментальная точность "
                    "не подменяет доказательство."
                ),
                "Проверенный формальный материал пока ограничен вводной рамкой.",
            ),
        )
    return (
        Explanation(
            "human",
            "Human",
            "Why it matters",
            (
                f"{subject} is one instrument, not a ready-made answer. This "
                "level explains the idea without requiring mathematical training."
            ),
            "An intuitive map of the topic.",
        ),
        Explanation(
            "technical",
            "Technical",
            "How the computational approach is structured",
            (
                "The technical level fixes inputs, architecture, metrics, "
                "baselines and comparison limits before results are inspected."
            ),
            "Implementation details will accompany a reproducible protocol.",
        ),
        Explanation(
            "scientific",
            "Scientific",
            "The formal boundary of the claim",
            (
                "The formal level ties definitions and claims to primary "
                "sources. Experimental accuracy does not replace proof."
            ),
            "Reviewed formal material is currently limited to this framing.",
        ),
    )


METHODS: dict[str, dict[str, MethodCopy]] = {
    "ru": {
        "kan": MethodCopy(
            "kan",
            "Kolmogorov–Arnold Networks",
            "KAN",
            "Семейство сетей с обучаемыми одномерными функциями на рёбрах.",
            "Исследовать аппроксимацию и представление структуры рядом с baselines.",
            "Интерпретируемость и преимущество нельзя выводить из одной визуализации.",
            _explanations("ru", "KAN"),
        ),
        "mlp": MethodCopy(
            "mlp",
            "Многослойный перцептрон",
            "MLP",
            "Базовая нейросетевая архитектура и обязательная точка сравнения.",
            "Дать понятный и сопоставимый neural baseline.",
            "Сравнение требует согласованных параметров, budget и метрик.",
            _explanations("ru", "MLP"),
        ),
        "pinn": MethodCopy(
            "pinn",
            "Physics-Informed Neural Networks",
            "PINN",
            "Нейросетевой подход, включающий уравнения в функцию потерь.",
            "Исследовать численные постановки рядом с классическими методами.",
            "Малая невязка не гарантирует точность решения на всей области.",
            _explanations("ru", "PINN"),
        ),
        "comparison": MethodCopy(
            "comparison",
            "Сравнительные эксперименты",
            "Сравнения",
            "Протоколы, где метрики и критерии определены заранее.",
            "Сопоставлять качество, время, память, устойчивость и экстраполяцию.",
            "Один benchmark не устанавливает универсальное превосходство.",
            _explanations("ru", "Сравнительный эксперимент"),
        ),
    },
    "en": {
        "kan": MethodCopy(
            "kan",
            "Kolmogorov–Arnold Networks",
            "KAN",
            "A network family with learnable univariate functions on edges.",
            "Study approximation and structural representation beside baselines.",
            "Interpretability or superiority cannot follow from one visualisation.",
            _explanations("en", "KAN"),
        ),
        "mlp": MethodCopy(
            "mlp",
            "Multilayer Perceptron",
            "MLP",
            "A baseline neural architecture and mandatory comparison point.",
            "Provide a clear, complexity-aware neural baseline.",
            "Fair comparison requires aligned parameters, budget and metrics.",
            _explanations("en", "MLP"),
        ),
        "pinn": MethodCopy(
            "pinn",
            "Physics-Informed Neural Networks",
            "PINN",
            "A neural approach that includes governing equations in the loss.",
            "Study numerical problems beside suitable classical methods.",
            "A small residual does not guarantee accuracy across the domain.",
            _explanations("en", "PINN"),
        ),
        "comparison": MethodCopy(
            "comparison",
            "Comparative experiments",
            "Comparisons",
            "Protocols with metrics and success criteria fixed in advance.",
            "Compare quality, time, memory, seed stability and extrapolation.",
            "One benchmark cannot establish universal superiority.",
            _explanations("en", "A comparative experiment"),
        ),
    },
}
