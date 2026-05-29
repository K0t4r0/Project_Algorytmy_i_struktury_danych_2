# Raport z postępów prac programistycznych – Tydzień 7

Siódmy tydzień realizacji projektu był momentem zamykającym cały proces tworzenia aplikacji i jednocześnie jednym z najbardziej wymagających etapów pracy. Po wielu tygodniach stopniowego rozwijania poszczególnych komponentów, dopracowywania detali oraz scalania kolejnych części systemu, zespół wszedł w fazę finalną, w której najważniejsze stało się już nie dodawanie nowych elementów, lecz dokładne sprawdzenie, poprawienie i uporządkowanie wszystkiego, co zostało wcześniej wykonane. Był to czas intensywnej koncentracji na jakości końcowej, stabilności działania oraz zgodności z założeniami projektowymi.

W ostatnim tygodniu pracy szczególnie wyraźnie można było zauważyć, jak duży postęp został osiągnięty na przestrzeni całego semestru. Aplikacja, która na początku projektu istniała głównie jako zbiór pomysłów, koncepcji i wstępnych szkiców, została doprowadzona do pełnej, spójnej postaci. Zespół skoncentrował się przede wszystkim na końcowych poprawkach, eliminacji błędów, testowaniu integracji pomiędzy modułami oraz upewnieniu się, że wszystkie funkcje działają zgodnie z oczekiwaniami. Dzięki temu możliwe było domknięcie całości projektu w sposób uporządkowany i profesjonalny.

## Zakończenie projektu i usuwanie błędów

W mijającym tygodniu priorytetem było dokładne przeanalizowanie wszystkich zgłoszonych problemów oraz doprowadzenie kodu do możliwie najlepszej formy przed oddaniem końcowej wersji projektu. Zespół poświęcił wiele czasu na przegląd działania aplikacji, identyfikację drobnych nieprawidłowości oraz wprowadzenie ostatnich poprawek, które miały znaczenie dla ogólnej stabilności systemu. Choć były to już końcowe etapy prac, ich znaczenie okazało się bardzo duże, ponieważ właśnie na tym poziomie często ujawniają się problemy trudne do zauważenia podczas wcześniejszych faz implementacji.

Ostatnie niezbędne zmiany zostały wprowadzone w następujących plikach:

- `project/algorithms/min_cost_max_flow.py`
- `project/algorithms/shortest_path.py`
- `project/ui/compression_page.py`
- `project/ui/flow_page.py`
- `project/ui/hull_page.py`
- `project/ui/segment_page.py`

Każdy z tych elementów miał istotne znaczenie dla finalnego działania aplikacji, dlatego ich dopracowanie było kluczowe. Zespół zadbał o to, aby wszystkie zauważone błędy zostały dokładnie przeanalizowane, a następnie usunięte w sposób niepowodujący nowych komplikacji. W praktyce oznaczało to nie tylko poprawianie pojedynczych fragmentów kodu, ale również sprawdzanie, czy wprowadzone zmiany nie wpływają negatywnie na inne części systemu. Taka ostrożność była szczególnie ważna na końcowym etapie projektu, kiedy każda poprawka musiała być dobrze przemyślana i spójna z całym mechanizmem aplikacji.

Dzięki tym działaniom udało się wyeliminować wszystkie istotne problemy, które mogłyby wpłynąć na stabilność lub funkcjonalność aplikacji. Zespół konsekwentnie dopracowywał zarówno warstwę logiczną, jak i warstwę użytkową, aby końcowy efekt był nie tylko poprawny technicznie, ale również przejrzysty i wygodny w obsłudze. Ostatecznie kod został uporządkowany, a projekt nabrał pełnej, dopracowanej formy.

## Testy końcowe i przygotowanie do oddania

Po zakończeniu prac naprawczych przyszedł czas na szczegółowe testy wszystkich modułów. Był to jeden z najważniejszych etapów całego tygodnia, ponieważ pozwalał zweryfikować, czy wszystkie wcześniej wprowadzone elementy rzeczywiście współpracują ze sobą tak, jak zakładano. Testowanie obejmowało zarówno poszczególne funkcje, jak i cały przepływ działania aplikacji, dzięki czemu możliwe było sprawdzenie jej nie tylko fragmentarycznie, ale również jako całościowego rozwiązania.

Testy objęły następujące pliki:

- `project/tests/test_classes_and_data.py`
- `project/tests/test_compression_manager.py`
- `project/tests/test_generator.py`
- `project/tests/test_huffman.py`
- `project/tests/test_hull.py`
- `project/tests/test_min_cost_max_flow.py`
- `project/tests/test_royal_border_patrol.py`
- `project/tests/test_search.py`
- `project/tests/test_segment.py`
- `project/tests/test_shortest_path.py`

Zakres testów był szeroki i obejmował praktycznie wszystkie najważniejsze obszary funkcjonalne projektu. Zespół skupił się nie tylko na sprawdzaniu poprawności wyników, ale również na ocenie zachowania aplikacji w różnych scenariuszach użycia. Szczególną uwagę poświęcono przypadkom brzegowym, integracji pomiędzy modułami oraz stabilności działania przy uruchamianiu kolejnych funkcji. Dzięki temu końcowa weryfikacja była naprawdę kompleksowa i pozwoliła uzyskać pewność, że program działa zgodnie z oczekiwaniami.

Wyniki testów potwierdziły, że aplikacja działa poprawnie, a wszystkie funkcjonalności zostały zrealizowane zgodnie z założeniami projektowymi. System przeszedł pomyślnie zarówno testy jednostkowe, jak i testy integracyjne, co stanowi bardzo ważny dowód na to, że cały proces tworzenia został przeprowadzony w sposób przemyślany i skuteczny. Ostateczna weryfikacja pokazała również, że wcześniejsze decyzje dotyczące architektury, podziału obowiązków oraz organizacji pracy zespołowej były trafne i pozwoliły osiągnąć spójny rezultat.

## Współpraca zespołowa w końcowej fazie projektu

W ostatnim tygodniu szczególnie widoczna była wartość dobrej współpracy wewnątrz zespołu. Na tym etapie nie chodziło już wyłącznie o rozwijanie nowych funkcji, lecz przede wszystkim o wzajemne sprawdzanie rezultatów pracy, szybkie reagowanie na problemy i wspólne podejmowanie decyzji dotyczących finalnych poprawek. Dzięki regularnej komunikacji możliwe było sprawne koordynowanie działań i unikanie niepotrzebnych opóźnień.

Każdy z członków zespołu miał swój udział w końcowym sukcesie projektu. Osoby odpowiedzialne za poszczególne moduły dopracowywały swoje fragmenty kodu, równocześnie konsultując je z resztą grupy, co pozwoliło zachować spójność całego systemu. Taki model pracy okazał się szczególnie skuteczny właśnie w fazie końcowej, ponieważ umożliwił szybkie wykrywanie nieścisłości i skuteczne ich usuwanie, zanim mogłyby wpłynąć na końcowy rezultat.

Warto podkreślić, że ostatni tydzień był także podsumowaniem całego procesu współpracy. Zespół nie tylko zrealizował postawione cele techniczne, lecz również wypracował bardzo dobrą organizację pracy, odpowiedzialny sposób działania i umiejętność wspólnego rozwiązywania problemów. To właśnie ten aspekt miał duże znaczenie dla sprawnego doprowadzenia projektu do końca.

## Podsumowanie

Siódmy tydzień zakończył cały cykl prac nad projektem i można go uznać za etap definitywnego zamknięcia realizacji aplikacji. Wszystkie planowane funkcjonalności zostały zaimplementowane, ostatnie błędy zostały usunięte, a końcowe testy potwierdziły poprawność działania systemu. Zespół doprowadził projekt do stanu, w którym aplikacja jest w pełni funkcjonalna, stabilna i gotowa do oddania.

Na tym etapie można z satysfakcją stwierdzić, że cały wysiłek włożony w kolejne tygodnie pracy przyniósł oczekiwany rezultat. Projekt został nie tylko ukończony, ale również dopracowany w taki sposób, aby spełniał wymagania zarówno pod względem technicznym, jak i użytkowym. Ostatni tydzień był więc nie tylko finałem prac, lecz także potwierdzeniem, że konsekwentna organizacja, regularna współpraca i systematyczne podejście pozwoliły osiągnąć zamierzony cel.

Aplikacja jest gotowa do prezentacji, oddania oraz dalszego wykorzystania zgodnie z założeniami projektu.  