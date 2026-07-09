package tictactoe.web.model;

public class CreateGameRequest {
    private boolean vsComputer;

    public CreateGameRequest(){}

    public boolean isVsComputer() {
        return vsComputer;
    }

    public void setVsComputer(boolean vsComputer) {
        this.vsComputer = vsComputer;
    }
}
