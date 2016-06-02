package br.ufpe.cin.jbc5;

class RunningInfo {

	enum Status {
		TORUN, PASS, FAIL;
	}

	long start;
	long end;
	Status result = Status.TORUN;

	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append(start).append(", ");
		sb.append(end).append(", ");
		sb.append(result.name());
		return sb.toString();
	}
}