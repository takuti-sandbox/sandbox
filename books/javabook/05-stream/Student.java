public class Student {
  private String name;
  private int score;

  public Student(String name, int score) {
    this.name = name;
    this.score = score;
  }

  public int getScore() {
    return score;
  }

  public String toString() {
    return "Student(" + name + ", " + score + ")";
  }
}
