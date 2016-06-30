package br.ufpe.cin.dchecker.model;

public interface CheckableInfo {

	boolean hasFailed();

	boolean hasOverlap(CheckableInfo other);

	boolean isSameHostVM(CheckableInfo other);

	long finishedTime();

	long startTime();

	String name();

	String hostVm();
}
