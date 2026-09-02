import random
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

# ==================== ENUMS ====================

class CollegeDivision(Enum):
    D1 = 1
    D2 = 2
    D3 = 3

class AwardType(Enum):
    MVP = "MVP"
    FINALS_MVP = "Finals MVP"
    ALL_STAR = "All-Star"
    ALL_NBA = "All-NBA"
    DEFENSIVE_PLAYER_OF_YEAR = "Defensive Player of the Year"
    ROOKIE_OF_THE_YEAR = "Rookie of the Year"
    SIXTH_MAN = "Sixth Man of the Year"
    MIP = "Most Improved Player"

class GameResult(Enum):
    WIN = 1
    LOSS = 0

# ==================== DATA CLASSES ====================

@dataclass
class PlayerStats:
    """Spielerstatistiken pro Spiel"""
    points: int = 0
    rebounds: int = 0
    assists: int = 0
    steals: int = 0
    blocks: int = 0
    field_goal_percentage: float = 0.0
    three_point_percentage: float = 0.0
    free_throw_percentage: float = 0.0
    turnovers: int = 0
    minutes_played: int = 0
    
    def get_rating(self) -> float:
        """Berechnet ein Rating basierend auf Stats"""
        return (self.points * 0.3 + self.rebounds * 0.15 + self.assists * 0.2 + 
                self.steals * 0.1 + self.blocks * 0.1 + 
                (self.field_goal_percentage / 100) * 10)

@dataclass
class Game:
    """Ein einzelnes Spiel"""
    opponent: str
    result: GameResult
    player_stats: PlayerStats
    game_date: str
    season: int

@dataclass
class SeasonStats:
    """Saisonstatistiken eines Spielers"""
    season: int
    games_played: int = 0
    points_per_game: float = 0.0
    rebounds_per_game: float = 0.0
    assists_per_game: float = 0.0
    field_goal_percentage: float = 0.0
    three_point_percentage: float = 0.0
    free_throw_percentage: float = 0.0
    minutes_per_game: float = 0.0
    wins: int = 0
    
    def calculate_efficiency(self) -> float:
        """PER-ähnlicher Efficiency-Rating"""
        return (self.points_per_game * 0.4 + 
                self.rebounds_per_game * 0.2 + 
                self.assists_per_game * 0.3 +
                (self.field_goal_percentage / 100) * 5)

@dataclass
class Award:
    """Ein Award/Auszeichnung"""
    award_type: AwardType
    season: int
    team: str
    description: str = ""

@dataclass
class Player:
    """Der Spieler"""
    name: str
    overall_rating: int
    age: int
    height_cm: int
    weight_kg: int
    position: str
    
    # College-Informationen
    college_name: str = "None"
    college_division: Optional[CollegeDivision] = None
    college_seasons: int = 0
    college_stats: List[SeasonStats] = field(default_factory=list)
    
    # NBA-Informationen
    draft_year: Optional[int] = None
    draft_pick: Optional[int] = None
    draft_team: Optional[str] = None
    nba_team: Optional[str] = None
    nba_seasons: int = 0
    nba_stats: List[SeasonStats] = field(default_factory=list)
    
    # Games
    games: List[Game] = field(default_factory=list)
    
    # Awards
    awards: List[Award] = field(default_factory=list)
    
    def add_award(self, award_type: AwardType, season: int, team: str):
        """Fügt einen Award hinzu"""
        award = Award(award_type, season, team)
        self.awards.append(award)
        print(f"🏆 {self.name} erhielt den {award_type.value} in Saison {season}!")
    
    def get_career_stats(self) -> Dict:
        """Gibt Career-Übersicht zurück"""
        return {
            "name": self.name,
            "position": self.position,
            "college": f"{self.college_name} ({self.college_division.name if self.college_division else 'N/A'})",
            "draft": f"Year {self.draft_year}, Pick {self.draft_pick}, Team {self.draft_team}" if self.draft_year else "Undrafted",
            "awards": len(self.awards),
            "nba_seasons": self.nba_seasons,
            "career_nba_ppg": self._calculate_career_ppg(),
        }
    
    def _calculate_career_ppg(self) -> float:
        """Berechnet Career PPG in der NBA"""
        if not self.nba_stats:
            return 0.0
        total_ppg = sum(season.points_per_game for season in self.nba_stats)
        return total_ppg / len(self.nba_stats)

# ==================== CAREER PHASE CLASSES ====================

class CollegeCareer:
    """Verwaltet die College-Phase"""
    
    def __init__(self, player: Player):
        self.player = player
        self.current_season = 0
        self.max_seasons = random.randint(1, 4)
        self.teams_d1 = ["Duke", "UNC", "Kentucky", "Kansas", "UCLA", "Michigan", "Ohio State", "Auburn", "Gonzaga", "Villanova"]
        self.teams_d2 = ["Cal Poly Pomona", "Ashland", "West Texas A&M", "South Dakota State", "Lenoir-Rhyne"]
        self.teams_d3 = ["Williams College", "Brandeis", "Amherst", "Middlebury", "Trinity"]
    
    def recruit_player(self) -> str:
        """Recruited den Spieler an ein College"""
        # Basierend auf Overall Rating wird die Division bestimmt
        if self.player.overall_rating >= 75:
            division = CollegeDivision.D1
            teams = self.teams_d1
        elif self.player.overall_rating >= 60:
            division = CollegeDivision.D2
            teams = self.teams_d2
        else:
            division = CollegeDivision.D3
            teams = self.teams_d3
        
        college = random.choice(teams)
        self.player.college_name = college
        self.player.college_division = division
        
        print(f"\n🎓 {self.player.name} wurde zu {college} ({division.name}) rekrutiert!")
        return college
    
    def simulate_college_season(self) -> SeasonStats:
        """Simuliert eine College-Saison"""
        self.current_season += 1
        season_num = self.current_season
        
        # Bestimme Minuten pro Spiel basierend auf Division und Jahr
        division_minutes = {
            CollegeDivision.D1: 25 + (season_num - 1) * 5,
            CollegeDivision.D2: 20 + (season_num - 1) * 4,
            CollegeDivision.D3: 15 + (season_num - 1) * 3,
        }
        
        avg_minutes = division_minutes[self.player.college_division]
        games_played = random.randint(28, 35)
        
        # Stats basierend auf Overall Rating
        avg_points = (self.player.overall_rating / 100) * 25 * (0.8 + season_num * 0.05)
        avg_rebounds = (self.player.overall_rating / 100) * 8
        avg_assists = (self.player.overall_rating / 100) * 3
        
        season_stats = SeasonStats(
            season=season_num,
            games_played=games_played,
            points_per_game=round(avg_points + random.uniform(-3, 3), 1),
            rebounds_per_game=round(avg_rebounds + random.uniform(-1, 1), 1),
            assists_per_game=round(avg_assists + random.uniform(-0.5, 0.5), 1),
            field_goal_percentage=round(40 + (self.player.overall_rating / 100) * 15 + random.uniform(-5, 5), 1),
            free_throw_percentage=round(70 + random.uniform(-10, 10), 1),
            minutes_per_game=round(avg_minutes, 1),
            wins=random.randint(15, 30)
        )
        
        self.player.college_stats.append(season_stats)
        self.player.college_seasons += 1
        
        print(f"\n📊 College Saison {season_num} für {self.player.name}:")
        print(f"   PPG: {season_stats.points_per_game} | RPG: {season_stats.rebounds_per_game} | APG: {season_stats.assists_per_game}")
        print(f"   FG%: {season_stats.field_goal_percentage}% | Spiele: {games_played}")
        
        return season_stats
    
    def player_should_go_pro(self) -> bool:
        """Bestimmt, ob der Spieler zum Draft ready ist"""
        if self.current_season < 2:
            return False
        
        # Basierend auf letzter Saison Performance
        if self.player.college_stats:
            last_season = self.player.college_stats[-1]
            performance_score = last_season.calculate_efficiency()
            
            # D1 Spieler können früher gehen
            if self.player.college_division == CollegeDivision.D1:
                return performance_score > 8 or self.current_season >= 3
            else:
                return self.current_season >= 3
        
        return self.current_season >= 4

# ==================== NBA DRAFT CLASS ====================

class DraftSystem:
    """Verwaltet den NBA Draft"""
    
    NBA_TEAMS = [
        "Lakers", "Celtics", "Warriors", "Heat", "Suns", "Mavericks",
        "Nuggets", "Clippers", "Bucks", "Nets", "76ers", "Knicks",
        "Grizzlies", "Kings", "Pelicans", "Raptors", "Pacers", "Cavaliers",
        "Bulls", "Pistons", "Rockets", "Spurs", "Timberwolves", "Blazers",
        "Hawks", "Hornets", "Magic", "Wizards", "Thunder", "Jazz"
    ]
    
    def __init__(self, player: Player):
        self.player = player
    
    def calculate_draft_position(self) -> int:
        """Berechnet Draft Position basierend auf College Performance"""
        if not self.player.college_stats:
            return random.randint(20, 60)
        
        # Berechne Average Efficiency
        avg_efficiency = sum(s.calculate_efficiency() for s in self.player.college_stats) / len(self.player.college_stats)
        
        # Basis auf Division
        division_bonus = {
            CollegeDivision.D1: 0,
            CollegeDivision.D2: 15,
            CollegeDivision.D3: 25,
        }
        
        position = 30 + division_bonus[self.player.college_division] - (avg_efficiency * 2)
        position = max(1, min(60, int(position)))
        
        return position
    
    def draft_player(self, draft_year: int):
        """Draftet den Spieler"""
        pick = self.calculate_draft_position()
        team = random.choice(self.NBA_TEAMS)
        
        self.player.draft_year = draft_year
        self.player.draft_pick = pick
        self.player.draft_team = team
        self.player.nba_team = team
        
        print(f"\n🏀 {self.player.name} wurde in Year {draft_year}, Pick {pick} von {team} gedraftet!")
        
        # Spieler erhält Rookie of the Year Chance in erster Saison
        return team

# ==================== NBA CAREER CLASS ====================

class NBACareer:
    """Verwaltet die NBA-Karriere"""
    
    def __init__(self, player: Player):
        self.player = player
        self.current_season = 0
    
    def simulate_nba_season(self) -> SeasonStats:
        """Simuliert eine NBA Saison"""
        self.current_season += 1
        self.player.nba_seasons += 1
        season_num = self.current_season
        
        # Minuten pro Spiel basierend auf Draft Pick und Alter
        base_minutes = 12
        if self.player.draft_pick <= 10:
            base_minutes = 28
        elif self.player.draft_pick <= 20:
            base_minutes = 22
        elif self.player.draft_pick <= 30:
            base_minutes = 18
        else:
            base_minutes = 12
        
        # Verbesserung mit Jahren
        mpg = base_minutes + (season_num - 1) * 1.5
        
        # Stats
        ppg_multiplier = 1.0 + (season_num - 1) * 0.1
        
        avg_points = (self.player.overall_rating / 100) * 20 * ppg_multiplier + random.uniform(-5, 5)
        avg_rebounds = (self.player.overall_rating / 100) * 5
        avg_assists = (self.player.overall_rating / 100) * 2.5
        
        season_stats = SeasonStats(
            season=season_num,
            games_played=random.randint(50, 82),
            points_per_game=round(max(0, avg_points), 1),
            rebounds_per_game=round(max(0, avg_rebounds), 1),
            assists_per_game=round(max(0, avg_assists), 1),
            field_goal_percentage=round(42 + random.uniform(-5, 8), 1),
            free_throw_percentage=round(75 + random.uniform(-10, 10), 1),
            minutes_per_game=round(mpg, 1),
            wins=random.randint(20, 70)
        )
        
        self.player.nba_stats.append(season_stats)
        
        print(f"\n🎮 NBA Saison {season_num} ({self.player.nba_team}):")
        print(f"   PPG: {season_stats.points_per_game} | RPG: {season_stats.rebounds_per_game} | APG: {season_stats.assists_per_game}")
        print(f"   MPG: {season_stats.minutes_per_game} | Spiele: {season_stats.games_played}")
        
        return season_stats
    
    def check_awards(self, season: int):
        """Prüft auf Awards nach jeder Saison"""
        if not self.player.nba_stats or len(self.player.nba_stats) < season:
            return
        
        season_stats = self.player.nba_stats[season - 1]
        
        # Rookie of the Year (nur erste Saison)
        if season == 1:
            if season_stats.points_per_game >= 15:
                self.player.add_award(AwardType.ROOKIE_OF_THE_YEAR, season, self.player.nba_team)
        
        # All-Star (PPG >= 20 oder hohe Stats)
        if season_stats.points_per_game >= 20:
            self.player.add_award(AwardType.ALL_STAR, season, self.player.nba_team)
        
        # All-NBA (PPG >= 25 und hohe Efficiency)
        if season_stats.points_per_game >= 25 and season_stats.calculate_efficiency() >= 15:
            self.player.add_award(AwardType.ALL_NBA, season, self.player.nba_team)
        
        # MVP (elite stats in guter Saison)
        if (season_stats.points_per_game >= 28 and 
            season_stats.calculate_efficiency() >= 18 and
            season_stats.wins >= 60):
            self.player.add_award(AwardType.MVP, season, self.player.nba_team)
        
        # Finals MVP (zufälliger Bonus wenn starke Stats)
        if season_stats.points_per_game >= 27 and random.random() < 0.15:
            self.player.add_award(AwardType.FINALS_MVP, season, self.player.nba_team)
        
        # Most Improved Player
        if season >= 3:
            prev_season = self.player.nba_stats[season - 2]
            improvement = season_stats.points_per_game - prev_season.points_per_game
            if improvement >= 8 and season_stats.points_per_game >= 20:
                self.player.add_award(AwardType.MIP, season, self.player.nba_team)
        
        # Sixth Man of the Year (weniger als 25 MPG aber hohe Efficiency)
        if season_stats.minutes_per_game < 25 and season_stats.calculate_efficiency() >= 12:
            self.player.add_award(AwardType.SIXTH_MAN, season, self.player.nba_team)

# ==================== GAME MANAGER ====================

class CareerGameManager:
    """Hauptspiel-Manager"""
    
    def __init__(self):
        self.player: Optional[Player] = None
        self.game_year = 2024
    
    def create_player(self, name: str, position: str, height_cm: int = 200, weight_kg: int = 100) -> Player:
        """Erstellt einen neuen Spieler"""
        overall_rating = random.randint(55, 95)
        self.player = Player(
            name=name,
            overall_rating=overall_rating,
            age=17,
            height_cm=height_cm,
            weight_kg=weight_kg,
            position=position
        )
        print(f"\n✅ Spieler erstellt: {name}")
        print(f"   Position: {position} | Overall Rating: {overall_rating}")
        return self.player
    
    def start_college_career(self):
        """Startet die College-Karriere"""
        if not self.player:
            print("Fehler: Spieler nicht erstellt!")
            return
        
        college_career = CollegeCareer(self.player)
        college_career.recruit_player()
        
        # Simuliere College-Saisons
        while not college_career.player_should_go_pro():
            college_career.simulate_college_season()
            
            # Option: Früh gehen wenn sehr gut
            if college_career.current_season >= 2:
                quality = college_career.player.college_stats[-1].calculate_efficiency()
                if quality > 14 and random.random() < 0.4:
                    print(f"\n💡 {self.player.name} entscheidet sich, zum Draft zu gehen!")
                    break
        
        print(f"\n✅ College-Karriere abgeschlossen: {self.player.college_seasons} Saisons")
    
    def start_nba_draft(self):
        """Durchführt den NBA Draft"""
        if not self.player:
            print("Fehler: Spieler nicht erstellt!")
            return
        
        draft = DraftSystem(self.player)
        self.game_year += 1
        draft.draft_player(self.game_year)
    
    def start_nba_career(self, num_seasons: int = 5):
        """Startet die NBA-Karriere"""
        if not self.player:
            print("Fehler: Spieler nicht erstellt!")
            return
        
        nba_career = NBACareer(self.player)
        
        for season in range(1, num_seasons + 1):
            self.game_year += 1
            print(f"\n--- NBA Saison {season} ({self.game_year - 1}-{self.game_year}) ---")
            
            nba_career.simulate_nba_season()
            nba_career.check_awards(season)
            
            # Optional: Spieler-Entwicklung
            if random.random() < 0.3:
                self.player.overall_rating = min(99, self.player.overall_rating + random.randint(1, 3))
                print(f"⬆️  {self.player.name}'s Overall Rating ist gestiegen auf {self.player.overall_rating}!")
    
    def show_career_summary(self):
        """Zeigt eine Karrierezusammenfassung"""
        if not self.player:
            print("Fehler: Spieler nicht erstellt!")
            return
        
        print("\n" + "="*60)
        print("📋 CAREER SUMMARY".center(60))
        print("="*60)
        
        career = self.player.get_career_stats()
        for key, value in career.items():
            print(f"{key.upper():.<35} {value}")
        
        print("\n🏆 AWARDS:")
        if self.player.awards:
            for award in self.player.awards:
                print(f"   • {award.award_type.value} (Season {award.season}) - {award.team}")
        else:
            print("   Keine Awards erhalten")
        
        print("\n📊 NBA CAREER STATS:")
        if self.player.nba_stats:
            for season in self.player.nba_stats:
                print(f"   Season {season.season}: {season.points_per_game} PPG, {season.minutes_per_game} MPG, {season.games_played} GP")
        else:
            print("   Noch keine NBA-Saisons")
        
        print("="*60)

# ==================== MAIN GAME LOOP ====================

def main():
    """Hauptspiel-Loop"""
    manager = CareerGameManager()
    
    print("\n" + "="*60)
    print("🏀 NBA BASKETBALL CAREER MODE 🏀".center(60))
    print("="*60)
    
    # Spieler erstellen
    player_name = input("\nEnter your player name: ")
    player_position = input("Enter position (PG, SG, SF, PF, C): ").upper()
    
    manager.create_player(player_name, player_position)
    
    # College-Phase
    print("\n🎓 Starting College Career...")
    manager.start_college_career()
    
    # NBA Draft
    print("\n📢 Entering NBA Draft...")
    manager.start_nba_draft()
    
    # NBA-Phase
    print("\n🏀 Starting NBA Career...")
    num_seasons = int(input("How many NBA seasons do you want to simulate? (1-15): "))
    manager.start_nba_career(min(15, max(1, num_seasons)))
    
    # Zusammenfassung
    manager.show_career_summary()

if __name__ == "__main__":
    main()
