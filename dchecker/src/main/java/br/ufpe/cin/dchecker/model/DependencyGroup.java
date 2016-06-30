package br.ufpe.cin.dchecker.model;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

public class DependencyGroup {

	private CheckableInfo owner;
	private Set<CheckableInfo> group;

	public DependencyGroup(CheckableInfo from) {
		this.owner = from;
		this.group = new HashSet<CheckableInfo>();
		put(from);
	}

	public int size() {
		return this.group.size();
	}

	public void put(CheckableInfo dependency) {
		this.group.add(dependency);
	}

	public CheckableInfo getOwner() {
		return this.owner;
	}

	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		String lineSep = System.getProperty("line.separator");
		sb.append("Dependency Group: ").append(size()).append(lineSep);
		for (CheckableInfo dep : this.group) {
			sb.append(" => ").append(dep.name()).append(lineSep);
		}
		return sb.toString();
	}

	public boolean canJoin(DependencyGroup other) {
		return !Collections.disjoint(this.group, other.group);
	}

	public void join(DependencyGroup other) {
		this.group.addAll(other.group);
	}

}